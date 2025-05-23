mistral_1 = """
    Tu es un assistant expert en analyse sémantique et en inférence.

    Ta tâche est de déterminer si un exposé sommaire d’amendement est en lien, même de manière implicite ou indirecte, avec une idée politique ou conceptuelle.
    
    
    Tu dois suivre ces étapes :
    
    1. Lire l’exposé sommaire et en donner un bref résumé.
    2. Identifier les thèmes, préoccupations ou objectifs présents, même s'ils ne sont pas formulés explicitement.
    3. Lire la description de l’idée et résumer les concepts clés qu’elle porte.
    4. Comparer les deux et indiquer si l’idée est en lien (même implicite) avec l’exposé.
    
    Réponds uniquement à la fin par Oui ou Non.
        
    ---
    Idée : {IDEE}
    --- 

    ---
    Description de l’idée : {DESCRIPTION}
    ---

    ---
    Exposé sommaire : {EXPOSE_SOMMAIRE}
    ---
    
    Analyse :
    
    1. Résumé de l’exposé :
    2. Thèmes identifiés :
    3. Concepts de l’idée :
    4. Comparaison sémantique :
    5. L’exposé est-il en lien (même implicite) avec cette idée ?
    
    Réponds uniquement par : 'oui' (si l'idée décrite est en lien indirect ou direct avec le contenu de l'exposé sommaire), 'non' (sinon). 
    
    Ne donne aucune justification, seulement le terme demandé."
    ---
    """


prompt_test= """

    Instruction :

    Vous êtes un assistant chargé d'analyser la présence d'une idée dans un texte.

    Tâche :

    Étant donné :

    - Idée : {IDEE}
    - Description de l'idée : {DESCRIPTION}
    - Exposé sommaire : {EXPOSE_SOMMAIRE}

    Déterminez si l'idée décrite est présente dans l'exposé sommaire, que ce soit de manière explicite ou implicite.

    Répondez uniquement par :

    Oui
    Non

    Aucune autre information ou explication n'est requise."

"""



prompt_test_ch= """
    # Instruction :

    Vous êtes un assistant chargé d'analyser la présence d'une idée dans un texte. 
    
    Déterminez si l'idée décrite est présente dans le texte, que ce soit de manière explicite ou implicite.


    <<<
    Idée : {IDEE}
    >>>

    <<<
    Description de l'idée : {DESCRIPTION}
    >>>
    
    <<<
    Texte : {EXPOSE_SOMMAIRE}
    >>>

    Répondez uniquement par :
    Oui
    Non

    Aucune autre information ou explication n'est requise."
"""



prompt_exemple= """
    # Instruction :

    Vous êtes un assistant chargé d'analyser la présence d'une idée dans un texte. 
    
    Déterminez si l'idée décrite est présente dans le texte, que ce soit de manière explicite ou implicite.

    <<<
    Idée : {IDEE}
    >>>

    <<<
    Description de l'idée : {DESCRIPTION}
    >>>
    
    <<<
    Texte : {EXPOSE_SOMMAIRE}
    >>>

    # Exemple :
    - Idée : simplification des démarches administratives
    - Description de l'idée : réduire les réglementations environnementales et sanitaires. Simplifier les démarches administratives, démarches bureaucratiques chronophages qui sont des freins qui entravent le quotidien des agriculteurs.
    - Texte : Dans l’optique de renforcer l’efficacité du guichet unique et l’accompagnement des cédants et afin de rendre incontournable le dispositif France Services Agriculture pour tous les acteurs, il est proposé que l’attestation de passage à FSA constitue une pièce obligatoire du dossier de demande de retraite. \nLe parcours ainsi établi a fait l’objet d’un consensus à l’issue des concertations, régionales et nationale, menées en 2022-2023, et des recommandations du Conseil économique, social et environnemental. Cet accompagnement permet de répondre aux objectifs d’intérêt général de la\n politique agricole énoncés à l’article L. 1 du code rural et de la pêche.
    - Réponse: Non
    # Fin exemple

    Répondez uniquement par :
    Oui
    Non

    Aucune autre information ou explication n'est requise."
"""