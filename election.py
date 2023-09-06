from dataclasses import dataclass, field
import re


# The Candidate class features data of given candidate, including name, last name, number of votes, constituency
# and whether the candidate still participates in the election.
@dataclass
class Candidate:
    name: str
    last_name: str
    votes_count: int
    constituency: str
    participates_in_election: bool = True


# The Elector class contains data about en elector, including constituency and a list of candidates for whom
# the voter can cast a vote.
@dataclass
class Elector:
    constituency: str
    candidates: list[Candidate] = field(default_factory=lambda: [])


def main() -> None:
    c = Candidate('AAA', 'BBB', 0, '01')
    e = Elector('O1')
    print(c), print(e)

if __name__ == '__main__':
    main()