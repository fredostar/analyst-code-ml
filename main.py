
from mistralai.client import Mistral
from os import getenv

api_key = getenv("MISTRAL_API_KEY")

mistral_client = Mistral(api_key=api_key)


def main():
    print("Hello from analyst-code-ml!")

    question = "Peux tu me donner une fonction de tri bulle en python ?"
    modele = "mistral-tiny"

    response = mistral_client.chat.complete(
        model=modele,
        messages=[{"role":"user", "content":question}]
    )

    print("Réponse du modèle :")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
