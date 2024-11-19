CREATE_THESIS = """
CREATE (t:Thesis {
    uuid: randomUUID(),
    title: $title,
    text: $text,
    author_id: $author_id,
    rating: 0
})
RETURN t.uuid AS thesis_id
"""

CREATE_ANTITHESIS = """
MATCH (t:Thesis) WHERE t.uuid = $thesis_id
CREATE (at:Thesis {
    uuid: randomUUID(),
    title: $title,
    text: $text,
    author_id: $author_id,
    rating: 0
})-[:ANTITHESIS]->(t)
RETURN at.uuid AS thesis_id
"""

CREATE_SYNTHESIS = """
MATCH (t:Thesis), (at:Thesis)
WHERE t.uuid = $thesis_id AND at.uuid = $antithesis_id
CREATE (st:Thesis {
    uuid: randomUUID(),
    title: $title,
    text: $text,
    author_id: $author_id,
    rating: 0
})-[:THESIS_SYNTHESIS]->(t),
(st)-[:ANTITHESIS_SYNTHESIS]->(at)
RETURN st.uuid AS thesis_id
"""


GET_CREATE_THESIS_BY_ID = """
MATCH (t:Thesis)
WHERE t.uuid = $thesis_id
OPTIONAL MATCH (antithesis:Thesis)-[:ANTITHESIS]->(t)
OPTIONAL MATCH 
    (t)-[:THESIS_SYNTHESIS]->(thesis:Thesis),
    (t)-[:ANTITHESIS_SYNTHESIS]->(antithesis:Thesis)
RETURN t, thesis, antithesis
"""

# MATCH (t:Thesis)
# WHERE t.uuid = $thesis_id
# OPTIONAL MATCH (baseThesis:Thesis)<-[:ANTITHESIS]-(t)
# OPTIONAL MATCH (baseThesis)<-[:THESIS_SYNTHESIS]-(synthesis:Thesis),
#                (baseThesis)<-[:ANTITHESIS_SYNTHESIS]-(t)
# WITH
#     CASE
#         WHEN baseThesis IS NULL THEN t
#         ELSE baseThesis
#     END AS resolvedBaseThesis,
#     synthesis
# OPTIONAL MATCH (antithesis:Thesis)-[:ANTITHESIS]->(resolvedBaseThesis)
# RETURN resolvedBaseThesis AS thesis, antithesis, synthesis
