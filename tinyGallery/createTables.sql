DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS remarks;
DROP TABLE IF EXISTS likedPost;
DROP TABLE IF EXISTS tags;

CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userName TEXT UNIQUE NOT NULL,
    passWord TEXT NOT NULL,
    profileOpacity INTEGER DEFAULT 1,
    profileDefaultPage TEXT DEFAULT "images",
    NotificationStatus INTEGER DEFAULT 1,
    permissionGroup TEXT DEFAULT "user",
    date TEXT NOT NULL
);

CREATE TABLE posts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    postFilePath TEXT NOT NULL,
    type TEXT NOT NULL,
    coverFileType TEXT NOT NULL,
    postTitle TEXT NOT NULL,
    description TEXT NOT NULL,
    dots INTEGER DEFAULT 0,
    shareNum INTEGER DEFAULT 0,
    ViewNum INTEGER DEFAULT 0,
    nsfw INTEGER DEFAULT 0,
    userName TEXT NOT NULL,
    date TEXT NOT NULL,
    postUUID TEXT NOT NULL
);

CREATE TABLE remarks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    postUUID TEXT NOT NULL,
    userName TEXT NOT NULL,
    content TEXT NOT NULL,
    depth INTGER DEFAULT 1,
    remarkUUID TEXT NOT NULL,
    replyTo TEXT,
    date TEXT NOT NULL
);

CREATE TABLE likedPost(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userName TEXT NOT NULL,
    postUUID TEXT NOT NULL,
    likeStatus INTEGER DEFAULT 1
);

CREATE TABLE tags(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    postUUID TEXT NOT NULL,
    tag TEXT NOT NULL
)
