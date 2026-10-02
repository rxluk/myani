INSERT INTO roles (name) VALUES
    ('ADMIN'),
    ('USER');

-- login guest/password guest
INSERT INTO users (name, username, nickname, email, role_id, salt, password_hash)
VALUES (
    'Guest',
    'guest',
    'guest',
    'guest@guest',
    (SELECT id FROM roles WHERE name = 'USER'),
    '0f81c285d04b296f01806100f8115f53',
    'b6a6dfe38ff411ed9dd652770ce445eefd5906d9bf4fe4b618a0b765dc02a61f'
);

-- login naruto/password ramen123
INSERT INTO users (name, username, nickname, email, role_id, salt, password_hash)
VALUES (
    'Naruto Uzumaki',
    'naruto',
    'hokage',
    'naruto@konoha.com',
    (SELECT id FROM roles WHERE name = 'USER'),
    '13d3ec05d9d1ef2a4600848c29a711c4',
    '781aa49c8abb5ea6e1565880c4b536fdb8d66c26e04e90e6b227300c171b1b0f'
);

-- login light/password justice123
INSERT INTO users (name, username, nickname, email, role_id, salt, password_hash)
VALUES (
    'Light Yagami',
    'light',
    'kira',
    'light@deathnote.com',
    (SELECT id FROM roles WHERE name = 'USER'),
    'f5327054b5d072dd94e3caa901907c58',
    'a7afdf9512c6963dd3f89f4b0a5389f71da1802dd3d516a94ac666d73a5d4954'
);

-- login mikasa/password eren123
INSERT INTO users (name, username, nickname, email, role_id, salt, password_hash)
VALUES (
    'Mikasa Ackerman',
    'mikasa',
    'ackerman',
    'mikasa@paradis.com',
    (SELECT id FROM roles WHERE name = 'USER'),
    'a79eed5788f0aa3ddb857d9efc5fa553',
    '04208f5f5f594bdc67fc07482bae386a4b3b715795d7370e6ee574605d387647'
);

-- login edward/password alchemy123
INSERT INTO users (name, username, nickname, email, role_id, salt, password_hash)
VALUES (
    'Edward Elric',
    'edward',
    'fullmetal',
    'edward@amestris.com',
    (SELECT id FROM roles WHERE name = 'USER'),
    'df72c955c5e3f4cf14d28410ee17d540',
    'c9d92f46e7e131f0fec51c5138592ca77ef913bedff759b6267b1e9a5abd372a'
);

-- login ippo/password boxing123
INSERT INTO users (name, username, nickname, email, role_id, salt, password_hash)
VALUES (
    'Ippo Makunouchi',
    'ippo',
    'champion',
    'ippo@kamogawa.com',
    (SELECT id FROM roles WHERE name = 'USER'),
    '607154a7443cca96d9992ac11e3039af',
    '5caff41c34924d58c432ee0fc4cb265ea81735f847a34e05404bb8dca236dc80'
);

-- login kirito/password sword123
INSERT INTO users (name, username, nickname, email, role_id, salt, password_hash)
VALUES (
    'Kazuto Kirigaya',
    'kirito',
    'blackswordsman',
    'kirito@aincrad.com',
    (SELECT id FROM roles WHERE name = 'USER'),
    'c7ec48b7436f85deac903c9a98fbc612',
    '96a69ab433ff1f19328fcabc9aaff301d0b328cd33e2eca114b08c8518306e44'
);
