INSERT INTO watched_episode (user_id, episode_id, status, score)
SELECT u.id, e.id, 'WATCHED', 9
FROM episodes e
JOIN animes a ON a.id = e.anime_id
JOIN users u ON u.username = 'guest'
WHERE a.title = 'DEATH NOTE';

INSERT INTO watched_episode (user_id, episode_id, status, score)
SELECT u.id, e.id, 'WATCHED', NULL
FROM episodes e
JOIN animes a ON a.id = e.anime_id
JOIN users u ON u.username = 'guest'
WHERE a.title = 'NARUTO' AND e.number <= 50;

INSERT INTO watched_episode (user_id, episode_id, status, score)
SELECT u.id, e.id, 'WATCHED', 8
FROM episodes e
JOIN animes a ON a.id = e.anime_id
JOIN users u ON u.username = 'guest'
WHERE a.title = 'Noragami';

INSERT INTO watched_episode (user_id, episode_id, status, score)
SELECT u.id, e.id, 'WATCHED', 10
FROM episodes e
JOIN animes a ON a.id = e.anime_id
JOIN users u ON u.username = 'naruto'
WHERE a.title = 'NARUTO';

INSERT INTO watched_episode (user_id, episode_id, status, score)
SELECT u.id, e.id, 'WATCHED', 9
FROM episodes e
JOIN animes a ON a.id = e.anime_id
JOIN users u ON u.username = 'naruto'
WHERE a.title = 'NARUTO: Shippuuden' AND e.number <= 120;

INSERT INTO watched_episode (user_id, episode_id, status, score)
SELECT u.id, e.id, 'WATCHED', 10
FROM episodes e
JOIN animes a ON a.id = e.anime_id
JOIN users u ON u.username = 'light'
WHERE a.title = 'DEATH NOTE';

INSERT INTO watched_episode (user_id, episode_id, status, score)
SELECT u.id, e.id, 'WATCHED', 8
FROM episodes e
JOIN animes a ON a.id = e.anime_id
JOIN users u ON u.username = 'light'
WHERE a.title = 'Shingeki no Kyojin';

INSERT INTO watched_episode (user_id, episode_id, status, score)
SELECT u.id, e.id, 'WATCHED', NULL
FROM episodes e
JOIN animes a ON a.id = e.anime_id
JOIN users u ON u.username = 'light'
WHERE a.title = 'Shingeki no Kyojin Season 2' AND e.number <= 6;

INSERT INTO watched_episode (user_id, episode_id, status, score)
SELECT u.id, e.id, 'WATCHED', 10
FROM episodes e
JOIN animes a ON a.id = e.anime_id
JOIN users u ON u.username = 'mikasa'
WHERE a.title IN ('Shingeki no Kyojin', 'Shingeki no Kyojin Season 2', 'Shingeki no Kyojin Season 3');

INSERT INTO watched_episode (user_id, episode_id, status, score)
SELECT u.id, e.id, 'WATCHED', NULL
FROM episodes e
JOIN animes a ON a.id = e.anime_id
JOIN users u ON u.username = 'mikasa'
WHERE a.title = 'Shingeki no Kyojin Season 3 Part 2' AND e.number <= 5;

INSERT INTO watched_episode (user_id, episode_id, status, score)
SELECT u.id, e.id, 'WATCHED', 10
FROM episodes e
JOIN animes a ON a.id = e.anime_id
JOIN users u ON u.username = 'edward'
WHERE a.title = 'Hagane no Renkinjutsushi: FULLMETAL ALCHEMIST';

INSERT INTO watched_episode (user_id, episode_id, status, score)
SELECT u.id, e.id, 'WATCHED', 7
FROM episodes e
JOIN animes a ON a.id = e.anime_id
JOIN users u ON u.username = 'edward'
WHERE a.title = 'No Game No Life' AND e.number <= 8;

INSERT INTO watched_episode (user_id, episode_id, status, score)
SELECT u.id, e.id, 'WATCHED', 10
FROM episodes e
JOIN animes a ON a.id = e.anime_id
JOIN users u ON u.username = 'ippo'
WHERE a.title = 'Hajime no Ippo: THE FIGHTING!';

INSERT INTO watched_episode (user_id, episode_id, status, score)
SELECT u.id, e.id, 'WATCHED', NULL
FROM episodes e
JOIN animes a ON a.id = e.anime_id
JOIN users u ON u.username = 'ippo'
WHERE a.title = 'Hajime no Ippo: New Challenger' AND e.number <= 10;

INSERT INTO watched_episode (user_id, episode_id, status, score)
SELECT u.id, e.id, 'WATCHED', 8
FROM episodes e
JOIN animes a ON a.id = e.anime_id
JOIN users u ON u.username = 'ippo'
WHERE a.title = 'Inazuma Eleven' AND e.number <= 30;
