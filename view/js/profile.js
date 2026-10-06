const loggedUser = getLoggedUser();
const nickname = new URLSearchParams(window.location.search).get("nickname") ?? loggedUser?.nickname;

const profileStatus = document.getElementById("profile-status");
const profileHeader = document.getElementById("profile-header");
const stats = document.getElementById("stats");
const animesSection = document.getElementById("animes-section");
const animesSummary = document.getElementById("animes-summary");
const animesList = document.getElementById("animes-list");
const animesPagination = document.getElementById("animes-pagination");
const episodesSection = document.getElementById("episodes-section");
const episodesTitle = document.getElementById("episodes-title");
const episodesSummary = document.getElementById("episodes-summary");
const episodesList = document.getElementById("episodes-list");
const episodesPagination = document.getElementById("episodes-pagination");

let selectedAnime = null;

function renderUser(user, totalAnimes) {
  const isOwnProfile = loggedUser?.nickname === user.nickname;

  profileHeader.innerHTML = `
    <span class="avatar avatar--large profile-header__avatar">${escapeHtml(user.name[0].toUpperCase())}</span>
    <div>
      <h1 class="profile-header__name">${escapeHtml(user.name)}</h1>
      <p class="profile-header__handle">@${escapeHtml(user.nickname)}</p>
    </div>
    ${isOwnProfile ? `<button class="btn btn--ghost profile-header__logout" id="logout">Sair</button>` : ""}
  `;
  stats.innerHTML = `
    <div class="stats__item">
      <strong class="stats__value">${totalAnimes}</strong>
      <span class="stats__label">Animes assistidos</span>
    </div>
    <div class="stats__item">
      <strong class="stats__value">${formatDate(user.created_at)}</strong>
      <span class="stats__label">Membro desde</span>
    </div>
  `;
  profileHeader.hidden = false;
  stats.hidden = false;
  document.title = `${user.name} · Myani`;

  if (isOwnProfile) {
    document.getElementById("logout").addEventListener("click", () => {
      logout();
      window.location.href = "login.html";
    });
  }
}

function animeCard(anime) {
  const progress = Math.round((anime.watched_episodes / anime.total_episodes) * 100);
  return `
    <a class="card" href="#episodes-section" data-anime-id="${anime.id}" data-anime-title="${escapeHtml(anime.title)}">
      <div class="card__cover">
        <img class="card__image" src="${anime.cover_url}" alt="" loading="lazy">
        <div class="progress card__progress"><span class="progress__bar" style="width: ${progress}%"></span></div>
      </div>
      <h3 class="card__title">${escapeHtml(anime.title)}</h3>
      <p class="card__info">${anime.watched_episodes} de ${anime.total_episodes} episódios</p>
    </a>
  `;
}

function renderAnimes(result) {
  animesSummary.textContent = `${result.total} animes`;

  if (result.items.length === 0) {
    showMessage(animesList, "Este usuário ainda não assistiu nenhum anime.");
    return;
  }

  profileHeader.style.setProperty("--banner", `url("${result.items[0].cover_url}")`);
  animesList.className = "card-grid";
  animesList.innerHTML = result.items.map(animeCard).join("");
  renderPagination(animesPagination, result, loadAnimes);
}

async function loadAnimes(page) {
  try {
    renderAnimes(await api.findWatchedAnimes(nickname, page));
  } catch (error) {
    showMessage(animesList, error.message, "error");
  }
}

async function loadEpisodes(page) {
  episodesTitle.textContent = `Episódios de ${selectedAnime.title}`;
  episodesSection.hidden = false;
  showMessage(episodesList, "Carregando...", "loading");

  try {
    const result = await api.findWatchedEpisodes(nickname, selectedAnime.id, page);
    episodesSummary.textContent = `${result.total} episódios assistidos`;
    episodesList.innerHTML = episodeListHtml(result.items);
    renderPagination(episodesPagination, result, loadEpisodes);
    episodesSection.scrollIntoView({ behavior: "smooth" });
  } catch (error) {
    showMessage(episodesList, error.message, "error");
  }
}

animesList.addEventListener("click", (event) => {
  const card = event.target.closest("[data-anime-id]");
  if (card) {
    event.preventDefault();
    selectedAnime = { id: card.dataset.animeId, title: card.dataset.animeTitle };
    loadEpisodes(1);
  }
});

async function loadProfile() {
  if (!nickname) {
    window.location.href = "login.html";
    return;
  }

  showMessage(profileStatus, "Carregando...", "loading");
  try {
    const [user, animes] = await Promise.all([api.findUser(nickname), api.findWatchedAnimes(nickname, 1)]);
    profileStatus.innerHTML = "";
    renderUser(user, animes.total);
    renderAnimes(animes);
    animesSection.hidden = false;
  } catch (error) {
    showMessage(profileStatus, error.message, "error");
  }
}

loadProfile();
