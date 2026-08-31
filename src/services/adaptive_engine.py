class AdaptiveEngine:

    DIFFICULTY_ORDER = ["easy", "medium", "hard"]

    def decide_next_difficulty(
        self,
        score: int,
        current_difficulty: str,
    ) -> str:

        current_index = self.DIFFICULTY_ORDER.index(current_difficulty)

        if score <= 4:
            return self.DIFFICULTY_ORDER[
                max(0, current_index - 1)
            ]

        if score <= 7:
            return current_difficulty

        return self.DIFFICULTY_ORDER[
            min(2, current_index + 1)
        ]