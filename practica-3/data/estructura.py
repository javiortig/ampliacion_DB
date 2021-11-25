# This will be the structure of the json where data will be loaded:
# username, type that can be: [basic, company, university]
# publishings with title, body and date.

# After users, their relations:
# relations [{user 1, user 2, type}]. El type de relations puede ser family, friend, work, academic
# academic > work > family > friend

# And finally conversations/messages: TODO
{
    "users": [
        {    
            "username": "Pepito",
            "type": "basic",
            "publishings": [
                
            ]
        },
        {    
            "username": "Marga",
            "type": "basic",
            "publishings": [
                
            ]
        },
        {    
            "username": "Peluso",
            "type": "basic",
            "publishings": [
                {
                    "title": "Wook is brown",
                    "date": "ISO",
                    "body": "blablablablablablablablablablablablablablablablablablablabla"
                },
                {
                    "title": "Electricity is expensive",
                    "date": "ISO",
                    "body": "Corrupcion, escasez. Corrupcion, escasez. Corrupcion, escasez. Corrupcion, escasez. Corrupcion, escasez. Corrupcion, escasez. Corrupcion, escasez. Corrupcion, escasez. "
                },
            ]
        },
        {    
            "username": "Apple",
            "type": "company",
            "publishings": [
                
            ]
        },
        {
            "username": "UPM",
            "type": "university",
            "publishings": [

            ]
        }
    ],
    "relations": [
                {
                    "from": "Apple",
                    "to": "Pepito",
                    "type": "work"
                },
                {
                    "from": "Apple",
                    "to": "UPM",
                    "type": "academic"
                },
                {
                    "from": "Marga",
                    "to": "Pepito",
                    "type": "family"
                },
                {
                    "from": "Peluso",
                    "to": "Pepito",
                    "type": "friend"
                }
            ],
    # TODO: conversaciones y mensajes
}