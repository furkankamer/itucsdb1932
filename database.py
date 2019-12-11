from models.person import Person


class Database:
    def __init__(self):
        self.people = {}
        self._last_person_key = 0

    def add_person(self, person):
        self._last_person_key += 1
        self.people[self._last_person_key] = person
        return self._last_person_key

    def delete_person(self, person_key):
        if person_key in self.people:
            del self.people[person_key]

    def get_person(self, person_key):
        person = self.people.get(person_key)
        if person is None:
            return None
        person_ = Person(person.name, person.surname, title=person.title)
        return person_

    def get_people(self):
        people = []
        for person_key, person in self.people.items():
            person_ = Person(person.name, person.surname, title=person.title)
            people.append((person_key, person_))
        return people
