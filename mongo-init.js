db.auth('root', 'example')

db = db.getSiblingDB('zarinshop')

db.createUser(
        {
            user: "ZarinShop",
            pwd: "ZE4NGwd4t64nynR",
            roles: [
                {
                    role: "readWrite",
                    db: "zarinshop"
                }
            ]
        }
);