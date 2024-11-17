CREATE CONSTRAINT FOR (n:Thesis) REQUIRE n.uuid IS UNIQUE

// create primary thesis
CREATE (t:Thesis {
    uuid: randomUUID(),
    title: 'A',
    text: 'aaa',
    author_id: 0,
    rating: 0
})
RETURN t.uuid AS thesisId;

// create antithesis, have one relation: to thesis as his antithesis
MATCH (t:Thesis)
WHERE t.uuid = '{{thesis_id}}'
CREATE (at:Thesis {
    uuid: randomUUID(),
    title: 'B',
    text: 'bbb',
    author_id: 1,
    rating: 0
})-[:ANTITHESIS]->(t)
RETURN at.uuid AS thesisId;

// create synthesis, have two relations: to thesis and antithesis
MATCH (t:Thesis), (at:Thesis)
WHERE t.uuid = '{{thesis_id}}' 
  AND at.uuid = '{{antithesis_id}}'
CREATE (st:Thesis {
    uuid: randomUUID(),
    title: 'AB',
    text: 'abba',
    author_id: 3,
    rating: 0
})
-[:THESIS_SYNTHESIS]->(t),
(st)-[:ANTITHESIS_SYNTHESIS]->(at)
RETURN st.uuid AS thesisId;

// get thesis by id
MATCH (thesis:Thesis)
WHERE thesis.uuid = 'b3ed0fda-b706-44b8-b4a1-9b24359315f3'
OPTIONAL MATCH (antithesis:Thesis)-[:ANTITHESIS]->(thesis) // (+ optional all his antithesises)
RETURN thesis, antithesis

// get antithesis by id and his parent thesis
MATCH (antithesis:Thesis)
WHERE antithesis.uuid = '24e0482e-efd8-457d-886c-8b09f561852f'
MATCH (antithesis)-[:ANTITHESIS]->(thesis:Thesis)
OPTIONAL MATCH 
    (synthesis:Thesis)-[:ANTITHESIS_SYNTHESIS]->(antithesis), // (+ optional synthesis of them)
    (synthesis)-[:THESIS_SYNTHESIS]->(thesis)
RETURN thesis, antithesis, synthesis

// get synthesis by id with his thesis and antithesis
MATCH (synthesis:Thesis)
WHERE synthesis.uuid = '76c97c32-81ba-4487-93cc-b4f231815c7b'
MATCH 
    (synthesis)-[:THESIS_SYNTHESIS]->(thesis:Thesis),
    (synthesis)-[:ANTITHESIS_SYNTHESIS]->(antithesis:Thesis)
OPTIONAL MATCH (at:Thesis)-[:ANTITHESIS]->(synthesis) // (+ optional all his antithesises)
RETURN thesis, antithesis, synthesis, at

// list all, debug
MATCH (t:Thesis) RETURN t
