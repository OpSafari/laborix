from laborix.operations import builtins, generate, summarize


def test_generate_is_seeded() -> None:
    assert generate({}, {"count": 4}, 7) == generate({}, {"count": 4}, 7)


def test_summarize_executes_real_numpy() -> None:
    assert summarize({"values": [1, 2, 3]}, {}, 0) == {
        "mean": 2.0,
        "std": __import__("pytest").approx(0.8164965809),
    }


def test_builtin_registry_is_complete() -> None:
    assert builtins().names == ("synthetic.compare", "synthetic.generate", "synthetic.summarize")
