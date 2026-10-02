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