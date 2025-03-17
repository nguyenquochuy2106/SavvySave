CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    face_embedding BYTEA
);

CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    amount FLOAT,
    category VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
