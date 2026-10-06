const API_URL = "http://127.0.0.1:5000";
const PER_PAGE = 10;

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(API_URL + path, options);
  } catch {
    throw new Error("Não foi possível conectar à API.");
  }

  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(body.error ?? `Erro ${response.status}`);
  }
  return body;
}

function get(path, page) {
  return request(page ? `${path}?page=${page}&per_page=${PER_PAGE}` : path);
}

const api = {
  searchAnimes: (title, page) => get(`/animes/search/${encodeURIComponent(title)}`, page),
  findAnime: (animeId) => get(`/animes/${animeId}`),
  findAnimeEpisodes: (animeId, page) => get(`/animes/${animeId}/episodes`, page),
  searchUsers: (text, page) => get(`/users/search/${encodeURIComponent(text)}`, page),
  findUser: (nickname) => get(`/users/${encodeURIComponent(nickname)}`),
  findWatchedAnimes: (nickname, page) => get(`/users/${encodeURIComponent(nickname)}/animes`, page),
  findWatchedEpisodes: (nickname, animeId, page) =>
    get(`/users/${encodeURIComponent(nickname)}/animes/${animeId}/episodes`, page),
  login: (username, password) =>
    request("/users/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    }),
};

function getLoggedUser() {
  return JSON.parse(localStorage.getItem("user"));
}

function saveLoggedUser(user) {
  localStorage.setItem("user", JSON.stringify(user));
}

function logout() {
  localStorage.removeItem("user");
}

function escapeHtml(text) {
  return String(text ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function formatDate(date) {
  return date.slice(0, 10).split("-").reverse().join("/");
}

function showMessage(container, text, type = "empty") {
  container.className = "";
  container.innerHTML = `<p class="status-message status-message--${type}">${escapeHtml(text)}</p>`;
}

function renderPagination(container, result, goToPage) {
  if (result.total_pages <= 1) {
    container.innerHTML = "";
    return;
  }

  container.innerHTML = `
    <button class="btn btn--ghost" data-page="${result.page - 1}" ${result.page <= 1 ? "disabled" : ""}>Anterior</button>
    <span class="pagination__label">Página ${result.page} de ${result.total_pages}</span>
    <button class="btn btn--ghost" data-page="${result.page + 1}" ${result.page >= result.total_pages ? "disabled" : ""}>Próxima</button>
  `;
  container.onclick = (event) => {
    const page = event.target.dataset.page;
    if (page) {
      goToPage(Number(page));
    }
  };
}

function episodeListHtml(episodes) {
  const items = episodes.map((episode) => {
    const details = [
      episode.air_date && `Exibido em ${formatDate(episode.air_date)}`,
      episode.watched_at && `Assistido em ${formatDate(episode.watched_at)}`,
      episode.score && `Nota ${episode.score}`,
    ].filter(Boolean);
    const title = episode.name === String(episode.number) ? `Episódio ${episode.number}` : episode.name;

    return `
      <li class="episode-list__item">
        <span class="episode-list__number">EP ${episode.number}</span>
        <div>
          <p class="episode-list__title">${escapeHtml(title)}</p>
          <p class="episode-list__meta">${details.join(" · ")}</p>
        </div>
      </li>
    `;
  });
  return `<ol class="episode-list">${items.join("")}</ol>`;
}
