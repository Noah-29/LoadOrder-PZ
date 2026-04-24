<div align="center">

# 📦 LoadOrder - Project Zomboid Mod Manager

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Project Zomboid](https://img.shields.io/badge/Game-Project%20Zomboid-orange)](https://projectzomboid.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Un outil puissant pour analyser, catégoriser et générer automatiquement l'ordre de chargement de vos mods Project Zomboid.**

---

[Fonctionnalités](#-fonctionnalités) • [Installation](#-installation) • [Configuration](#-configuration) • [Utilisation](#-utilisation)

</div>

## 🎯 Présentation

**LoadOrder** simplifie la vie. Il scanne vos fichiers, récupère les infos manquantes sur Steam et prépare vos fichiers de configuration en quelques secondes.

## ✨ Fonctionnalités

| Action | Description |
| :--- | :--- |
| 🔍 **Analyse Locale** | Scanne vos dossiers et extrait les données des fichiers `mod.info`. |
| 🌐 **Steam Scraping** | Télécharge les descriptions et noms réels via la Steam Community. |
| 🔗 **Gestion Dépendances** | Identifie automatiquement les mods requis par d'autres. |
| 🛠️ **Config Auto** | Génère les listes `Mod IDs`, `Workshop IDs` et `Maps` pour votre serveur. |

### 🗂️ Catégorisation Automatique
Le script trie vos mods selon 7 catégories essentielles pour la stabilité :
1. **Tiles** (Textures/Visuels)
2. **Maps** (Cartes personnalisées)
3. **Dépendances** (Frameworks)
4. **Ressources Système**
5. **Mods QOL** (Qualité de vie)
6. **Craft & Items**
7. **Véhicules**

> [!IMPORTANT]
> **⚠️ Attention sur le tri :** La précision de la catégorisation dépend entièrement des informations saisies par les créateurs de mods. Si un moddeur n'a pas spécifié de catégorie ou a mal rempli son fichier `mod.info`, le mod peut être mal classé. **Une vérification manuelle du fichier de sortie est donc fortement recommandée.**
---

## 🚀 Installation

1. **Clonez le dépôt :**
   ```bash
   git clone [https://github.com/votre-pseudo/LoadOrder.git](https://github.com/votre-pseudo/LoadOrder.git)
   cd LoadOrder
