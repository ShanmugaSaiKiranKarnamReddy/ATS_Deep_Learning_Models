
from neo4j import GraphDatabase, basic_auth
from csv import reader, writer
driver = GraphDatabase.driver("bolt://localhost:7687", auth= basic_auth(user = "neo4j", password = "Knowledge_graph"))


def find_node(tx, name):
    levels = []
    names = []
    result = tx.run("MATCH (a)"
                    "WHERE a.name = $name "
                    "RETURN a.level AS level, a.name AS name", name=name)
    for record in result:
        levels.append(record["level"])
        names.append(record["name"])
    return levels, names


def find_relation(tx, JDword, CVword):
    relation1 = []
    relation2 = []
    result1 = tx.run("Match (n)-[]->(m)"
                     "Where m.name= $JDword and n.name = $CVword "
                     "Return m.name AS name", JDword=JDword, CVword=CVword)
    result2 = tx.run("Match (m)-[]->(n)"
                     "Where m.name= $JDword and n.name = $CVword "
                     "Return m.name AS name", JDword=JDword, CVword=CVword)
    for record in result1:
        relation1.append(record["name"])
    for record in result2:
        relation2.append(record["name"])
    return relation1, relation2

def findscore(JDword,CVword):
    with driver.session() as session:
        jd_level, jd_name = session.read_transaction(find_node, JDword)
        cv_level, cv_name = session.read_transaction(find_node, CVword)
        relation_result1, relation_result2 = session.read_transaction(find_relation, JDword, CVword)

        if jd_name == [] or cv_name == []:
            score = 0
            return score

        elif jd_name == cv_name:
            score = 5
            return score

        else:
            for c in relation_result1:
                res = isinstance(c, str)
                if res == True:
                    print("relation exists, node= ", c)
                    if jd_level < cv_level:
                        score = 4
                        return score
                    elif cv_level < jd_level:
                        score = 3
                        return score
            for c in relation_result2:
                res = isinstance(c, str)
                if res == True:
                    print("relation exists, node= ", c)
                    if jd_level < cv_level:
                        score = 4
                        return score
                    elif cv_level < jd_level:
                        score = 3
                        return score
    driver.close()


with open('computer.csv', 'r',  encoding='utf8', errors='ignore') as read_obj:
    csv_reader = reader(read_obj)
    for row in csv_reader:
        JDword = row[1]
        CVword = row[0]

        with open('new1.csv', 'a',newline='', encoding='utf8', errors='ignore')as write_obj:
            csv_writer = writer(write_obj)
            score = findscore(JDword, CVword)
            print(JDword,CVword,score)
            csv_writer.writerow([JDword] + [CVword] + [score])