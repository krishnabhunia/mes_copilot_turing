import uuid


def generate_unique_identifier():
    return str(uuid.uuid4())


# Example usage
unique_id = generate_unique_identifier()
print(f"Generated unique identifier: {unique_id}")
