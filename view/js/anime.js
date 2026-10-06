const animeId = new URLSearchParams(window.location.search).get("id");
const animeStatus = document.getElementById("anime-status");
const hero = document.getElementById("hero");
const episodesSection = document.getElementById("episodes-section");
const episodesSummary = document.getElementById("episodes-summary");
const episodesList = document.getElementById("episodes-list");
const episodesPagination = document.getElementById("episodes-pagination");

function renderHero(anime, totalEpisodes) {
  const englishTitle = anime.title_english?.toLowerCase() === anime.title.toLowerCase() ? "" : anime.title_english;
  const details = [
    `${totalEpisodes} episódios`,
    anime.episode_duration && `${anime.episode_duration} min por episódio`,
    anime.is_finished ? "Finalizado" : "Em exibição",
  ].filter(Boolean);

  hero.style.setProperty("--banner", `url("${anime.cover_url}")`);
  hero.innerHTML = `
    <img class="hero__cover" src="${anime.cover_url}" alt="">
    <div class="hero__body">
      <span class="hero__eyebrow">${escapeHtml(englishTitle)}</span>
      <h1 class="hero__title">${escapeHtml(anime.title)}</h1>
      <p class="hero__meta">${details.join(" · ")}</p>
    </div>
  `;
  hero.hidden = false;
  document.title = `${anime.title} · Myani`;
}

function renderEpisodes(result) {
  episodesSummary.textContent = `${result.total} episódios`;
  episodesList.innerHTML = episodeListHtml(result.items);
  renderPagination(episodesPagination, result, loadEpisodes);
}

async function loadEpisodes(page) {
  showMessage(episodesList, "Carregando...", "loading");
  try {
    renderEpisodes(await api.findAnimeEpisodes(animeId, page));
    episodesSection.scrollIntoView({ behavior: "smooth" });
  } catch (error) {
    showMessage(episodesList, error.message, "error");
  }
}

async function loadAnime() {
  if (!animeId) {
    showMessage(animeStatus, "Anime não informado.", "error");
    return;
  }

  showMessage(animeStatus, "Carregando...", "loading");
  try {
    const [anime, episodes] = await Promise.all([api.findAnime(animeId), api.findAnimeEpisodes(animeId, 1)]);
    animeStatus.innerHTML = "";
    renderHero(anime, episodes.total);
    renderEpisodes(episodes);
    episodesSection.hidden = false;
  } catch (error) {
    showMessage(animeStatus, error.message, "error");
  }
}

loadAnime();
