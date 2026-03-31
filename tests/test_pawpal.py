from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    """Task completion: mark_complete() should set completed to True."""
    task = Task("Morning walk", 20, "daily", "high")
    assert task.completed == False

    task.mark_complete()

    assert task.completed == True


def test_add_task_increases_pet_task_count():
    """Task addition: adding a task to a Pet should increase its task count."""
    pet = Pet("Mochi", "dog", 3)
    assert len(pet.tasks) == 0

    pet.add_task(Task("Feed breakfast", 10, "daily", "high"))
    assert len(pet.tasks) == 1

    pet.add_task(Task("Play fetch", 25, "daily", "medium"))
    assert len(pet.tasks) == 2
