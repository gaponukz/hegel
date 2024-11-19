CREATE_THESIS = "CREATE (t:Thesis {uuid: randomUUID(), title: $title, text: $text, author_id: $author_id, rating: 0}) RETURN t.uuid AS thesis_id"

CREATE_ANTITHESIS = "MATCH (t:Thesis) WHERE t.uuid = $thesis_id CREATE (at:Thesis {uuid: randomUUID(), title: $title, text: $text, author_id: $author_id, rating: 0})-[:ANTITHESIS]->(t) RETURN at.uuid AS thesis_id"

CREATE_SYNTHESIS = "MATCH (t:Thesis), (at:Thesis) WHERE t.uuid = $thesis_id AND at.uuid = $antithesis_id CREATE (st:Thesis {uuid: randomUUID(), title: $title, text: $text, author_id: $author_id, rating: 0})-[:THESIS_SYNTHESIS]->(t), (st)-[:ANTITHESIS_SYNTHESIS]->(at) RETURN st.uuid AS thesis_id"
