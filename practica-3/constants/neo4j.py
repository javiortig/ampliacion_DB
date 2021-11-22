USERNAME = "neo4j"
PASSWORD =  "password"
ADDRESS = "bolt://localhost:7687"

'''
user nodes have this structure:
- Basic user: (:user {username: "Juan"})
- University user: (:user:university {username: "Utad"})
- Company user: (:user:company {username: "Apple"})

'''