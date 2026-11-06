from functools import wraps

def log_action(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"{self.name} → {func.__name__}")
        return func(self, *args, **kwargs)
    return wrapper

class Character:

    count = 0

    def __init__(self, name, hp=100, level=1):
        self.name = name
        self._hp = hp
        self.level = level

        Character.count += 1

    @property
    def hp(self):
        return self._hp

    @classmethod
    def from_string(cls, text):
        parts = text.split(";")
        name = parts[0]
        hp = int(parts[1]) if len(parts) > 1 else 100
        return cls(name, hp=hp)

    @staticmethod
    def is_valid_name(name):
        return 2 <= len(name) <= 20

    def __eq__(self, other):
        if isinstance(other, Character):
            return self.name == other.name and self.level == other.level
        return False

    def __str__(self):
        return f"{self.name} (Lv {self.level}, HP {self.hp})"

    @hp.setter
    def hp(self, value):

        self._hp = max(0, value)

    def take_damage(self, amount):
        self.hp -= amount

    @property
    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        target.take_damage(5)

    def __str__(self):
        return f"{self.name} (Lv {self.level}, HP {self.hp})"


if __name__ == "__main__":
    a = Character("Tariel")
    b = Character("Avtandil", hp=50)
    b.take_damage(70)

    print(a)
    print(b)
    print(b.is_alive)
    print(Character.count)




class Warrior(Character):
    def __init__(self, name, hp=100, level=1, strength=10):
        super().__init__(name, hp, level)
        self.strength = strength

    def attack(self, target):
        target.take_damage(self.strength)


class Mage(Character):
    def __init__(self, name, hp=100, level=1, mana=50):
        super().__init__(name, hp, level)
        self.mana = mana

    def attack(self, target):
        if self.mana >= 10:
            self.mana -= 10
            target.take_damage(20)
        else:
            super().attack(target)

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str} MP {self.mana}"



if __name__ == "__main__":
    t = Warrior("Tariel", hp=120, strength=15)
    n = Mage("Nestan", hp=80, mana=15)

    t.attack(n)
    print(n)    # Nestan (Lv 1, HP 65) MP 15

    n.attack(t)   # 20 ზიანი, mana-ს 5 რჩება
    n.attack(t)   # mana არ ჰყოფნის: 5 ზიანი
    print(t)    # Tariel (Lv 1, HP 95)


@classmethod
def from_string(cls, text):

    parts = text.split(";")
    name = parts[0]
    hp = int(parts[1]) if len(parts) > 1 else 100
    return cls(name, hp=hp)

@staticmethod
def is_valid_name(name):
    return 2 <= len(name) <= 20

def __eq__(self, other):
    if isinstance(other, Character):
        return self.name == other.name and self.level == other.level
    return False

class HealerMixin:
    def heal(self, target, amount):
        target.hp += amount


class Priest(HealerMixin, Mage):
    pass

if __name__ == "__main__":
    print(Priest.__mro__)

    p = Priest("Nestan", hp=60)
    w = Warrior.from_string("Tariel;120")

    p.heal(w, 30)
    print(w)
    print(type(w).__name__)
    print(Character.is_valid_name("T"))
    print(Character("A") == Character("A"))


class Inventory:
    def __init__(self):
        self.items = []

    def add(self, **item):
        self.items.append(item)

    def find(self, **filters):
        result = []
        for item in self.items:
            if all(item.get(k) == v for k, v in filters.items()):
                result.append(item)
        return result

    def __len__(self):
        return len(self.items)

if __name__ == "__main__":
    inv = Inventory()
    inv.add(name="sword", kind="weapon", power=10)
    inv.add(name="potion", kind="heal", power=30)

    print(len(inv))                  # 2
    print(inv.find(kind="weapon"))   # [{'name': 'sword', 'kind': 'weapon', 'power': 10}]
    print(inv.find(kind="heal", power=30))   # [{'name': 'potion', 'kind': 'heal', 'power': 30}]

    tariel = Warrior("Tariel", hp=120, strength=15)
    nestan = Mage("Nestan", hp=80, mana=50)

    tariel.attack(nestan)            # Tariel → attack
    print(nestan)            # Nestan (Lv 1, HP 65) MP 50
    print(nestan.is_alive)   # True
    print(Character.count)   # 2