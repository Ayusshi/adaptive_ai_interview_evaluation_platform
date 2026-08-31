from pathlib import Path


class KnowledgeRetriever:

    def __init__(self, knowledge_dir: str = "knowledge"):

        self.knowledge_dir = Path(knowledge_dir)

        self.documents = {}

        self._load_documents()

    def _load_documents(self):

        for file_path in self.knowledge_dir.glob("*.md"):

            competency = file_path.stem.replace(
                "_",
                " ",
            )

            self.documents[competency] = (
                file_path.read_text(
                    encoding="utf-8"
                )
            )

    def retrieve(
        self,
        competency: str,
        expected_concepts: list[str],
    ) -> str:

        competency_key = competency.lower()

        document = None

        for key, content in self.documents.items():

            if key.lower() == competency_key:
                document = content
                break

        if document is None:

            return ""

        relevant_sections = []

        sections = document.split("\n## ")

        for section in sections:

            section_lower = section.lower()

            for concept in expected_concepts:

                if concept.lower() in section_lower:

                    relevant_sections.append(section)

                    break

        if not relevant_sections:

            return document

        return "\n\n".join(
            relevant_sections
        )


if __name__ == "__main__":

    retriever = KnowledgeRetriever()

    context = retriever.retrieve(
        competency="RAG",
        expected_concepts=[
            "chunking",
            "embeddings",
            "retrieval",
        ],
    )

    print("\nRetrieved Knowledge:\n")
    print(context)