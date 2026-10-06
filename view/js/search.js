const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("search-input");
const tabs = document.querySelectorAll("[data-type]");
const summary = document.getElementById("summary");
const results = document.getElementById("results");
const pagination = document.getElementById("pagination");

const params = new URLSearchParams(window.location.search);
let type = params.get("type") === "user" ? "user" : "anime";
let query = params.get("q") ?? "";

function animeCard(anime) {
  return `
    <a class="card" href="anime.html?id=${anime.id}">
      <div class="card__cover"><img class="card__image" src="${anime.cover_url}" alt="" loading="lazy"></div>
      <h3 class="card__title">${escapeHtml(anime.title)}</h3>
      <p class="card__info">${anime.total_episodes} episódios</p>
    </a>
  `;
}

function userCard(user) {
  return `
    <a class="user-card" href="profile.html?nickname=${encodeURIComponent(user.nickname)}">
      <span class="avatar">${escapeHtml(user.name[0].toUpperCase())}</span>
      <div>
        <p class="user-card__name">${escapeHtml(user.name)}</p>
        <p class="user-card__handle">@${escapeHtml(user.nickname)}</p>
      </div>
    </a>
  `;
}

async function search(page = 1) {
  summary.textContent = "";
  pagination.innerHTML = "";

  if (!query) {
    showMessage(results, "Digite algo para buscar.");
    return;
  }

  showMessage(results, "Carregando...", "loading");
  try {
    const result = type === "anime" ? await api.searchAnimes(query, page) : await api.searchUsers(query, page);
    summary.textContent = `${result.total} resultado(s)`;

    if (result.items.length === 0) {
      showMessage(results, "Nada encontrado.");
      return;
    }

    results.className = type === "anime" ? "card-grid" : "user-list";
    results.innerHTML = result.items.map(type === "anime" ? animeCard : userCard).join("");
    renderPagination(pagination, result, search);
  } catch (error) {
    showMessage(results, error.message, "error");
  }
}

function selectTab(selectedType) {
  type = selectedType;
  tabs.forEach((tab) => tab.classList.toggle("is-active", tab.dataset.type === type));
  searchInput.placeholder = type === "anime" ? "Buscar anime pelo título..." : "Buscar perfil pelo nome ou nickname...";
}

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    selectTab(tab.dataset.type);
    search();
  });
});

searchForm.addEventListener("submit", (event) => {
  event.preventDefault();
  query = searchInput.value.trim();
  search();
});

searchInput.value = query;
selectTab(type);
search();
