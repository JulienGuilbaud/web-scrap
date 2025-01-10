# Automatisation et services de protection anti-bot : Un Défi

**Important :**

* **Conditions d'utilisation :** Respectez toujours les conditions d'utilisation de services de protection anti-bot et du site web que vous automatisez.
* **Éthique :** Utilisez Selenium de manière responsable et évitez de surcharger les serveurs avec des requêtes excessives.
* **Évolution :** Les techniques de détection des bots sont en constante évolution.  Restez informé des dernières pratiques et adaptez votre approche en conséquence.

L'utilisation de robot avec des sites protégés par services de protection anti-bot peut être complexe en raison des mesures anti-bot de services de protection anti-bot.

Résultat avec l'ancien code utilisant selenium avec un VPN activé ou non :

![Résultat avec VPN ce n'est pas mon ip local lol](./assets/2025-01-09_12-03.png)


La première page s'ouvre correctement, mais à la seconde, tout se bloque.

## Navigation avec navigation_selenium.py

En résumé, ce script permet d'ouvrir automatiquement une série de liens, chacun dans une nouvelle session de navigateur. L'utilisation de temps d'attente aléatoires et d'options de configuration du navigateur vise à rendre le comportement du script moins prévisible et à contourner les mécanismes de détection de bots, notamment ceux mis en place par services de protection anti-bot.

## Scrap 

## environnement de dev
Python 3.12.4
Selenium 4.1
