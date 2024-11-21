CREATE INDEX FOR (n:Thesis) ON (n.uuid)

MERGE (:Placeholder)-[:ANTITHESIS]->(:Placeholder)
MERGE (:Placeholder)-[:ANTITHESIS_SYNTHESIS]->(:Placeholder)
MERGE (:Placeholder)-[:THESIS_SYNTHESIS]->(:Placeholder)
MATCH (n:Placeholder) DETACH DELETE n
