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

// get all info by id
MATCH (selected:Thesis)
WHERE selected.uuid = '{{thesis_id}}'
OPTIONAL MATCH (selected)-[:ANTITHESIS]->(antithesis_thesis:Thesis)
OPTIONAL MATCH 
    (selected)-[:THESIS_SYNTHESIS]->(synthesis_thesis:Thesis),
    (selected)-[:ANTITHESIS_SYNTHESIS]->(synthesis_antithesis:Thesis)
RETURN selected, antithesis_thesis, synthesis_thesis, synthesis_antithesis

// list all, debug
MATCH (t:Thesis) RETURN t
