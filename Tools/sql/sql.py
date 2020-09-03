with open ('agents.txt','r') as reader:
    agents = reader.read().split('\n')
    for agent in agents:
        query = 'INSERT INTO AGENTS(USERAGENT) VALUES ("{}");'.format(agent)
        with open('import.sql','a') as writer:
            writer.write(query+'\n')
#with open ('Categories.txt','r') as reader:
#    categories = reader.read().split('\n')
#    for category in categories:
#        cat_name = category.split('/')[2]
#        query = 'INSERT INTO AGENTS(CATEGORY_LINK,CATEGORY_NAME) VALUES ("{}", "{}");'.format(category,cat_name)
#        with open('import_categories.sql','a') as writer:
#            writer.write(query+'\n')