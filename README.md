# 🐔 PREVENT Program Dashboard - Production

## 🎯 Objectif

Dashboard sécurisé pour le programme PREVENT (Poultry Health in Africa) avec données chargées depuis Google Drive et authentification pour la Gates Foundation.

## 🔒 Sécurité

### Architecture Sécurisée
- 🔐 **Authentification** par mot de passe
- 📊 **Données externes** (Google Drive) 
- 🔒 **Aucune donnée sensible** dans le code source
- 🛡️ **Chiffrement HTTPS** pour tous les transferts

### Protection des Données
- ✅ **Code source public** (aucune donnée sensible)
- ✅ **Données privées** sur Google Drive
- ✅ **Secrets** dans Streamlit Cloud uniquement
- ✅ **Double authentification** (URL + mot de passe)

## 📊 Métriques Principales

- 🌍 **9 pays** couverts en Afrique
- 🏥 **23,159 visites** de fermes effectuées
- 📈 **11.4x croissance** du programme (2022-2024)
- 🩺 **68.3% réduction** de la mortalité W1
- 💊 **39.1% réduction** de l'usage d'antibiotiques

## 🚀 Déploiement

### Prérequis
- Repository GitHub public
- Compte Streamlit Cloud
- URLs Google Drive configurées (contactez l'administrateur)

### Configuration Streamlit Cloud

Dans "Advanced settings" > "Secrets" :
```toml
[passwords]
gates_foundation = "CONTACTEZ_ADMIN_POUR_MOT_DE_PASSE"
admin = "CONTACTEZ_ADMIN_POUR_MOT_DE_PASSE"

[data_urls]
farm_visits_url = "CONTACTEZ_ADMIN_POUR_URL_GOOGLE_DRIVE"
results_sanitaire = "CONTACTEZ_ADMIN_POUR_URL_GOOGLE_DRIVE"
results_zootechnique = "CONTACTEZ_ADMIN_POUR_URL_GOOGLE_DRIVE"
results_portee = "CONTACTEZ_ADMIN_POUR_URL_GOOGLE_DRIVE"
results_synthese = "CONTACTEZ_ADMIN_POUR_URL_GOOGLE_DRIVE"

[app_config]
app_name = "PREVENT Dashboard"
organization = "CEVA - Gates Foundation"
contact_email = "CONTACTEZ_ADMIN"
```

### Étapes de Déploiement

1. **Push vers GitHub** (repository public)
2. **Configurer Streamlit Cloud** :
   - Repository : `Matosa33/prevent-dashboard-gates`
   - Main file : `app.py`
   - Secrets : Contactez l'administrateur pour la configuration
3. **Déployer** et tester

## 📋 Fonctionnalités

### Interface Sécurisée
- 🔐 Écran de connexion avec mot de passe
- 🎨 Interface moderne Gates Foundation
- 🚪 Déconnexion sécurisée

### Analyses Disponibles
- 📊 **Impact Sanitaire** - Mortalité et antibiotiques
- 🗺️ **Portée Géographique** - Distribution par pays
- 📈 **Évolution Temporelle** - Tendances et croissance
- 🔍 **Sécurité & Traçabilité** - Informations techniques

### Sécurité Renforcée
- 🔒 Chargement sécurisé depuis Google Drive
- 🛡️ Authentification à deux niveaux
- 🔐 Aucune donnée en dur dans le code
- 📊 Traçabilité complète des sources

## 🔧 Architecture

### Flux de Données
```
Google Drive (privé) → Streamlit Cloud → Dashboard (authentifié)
```

### Niveaux de Sécurité
1. **URLs Google Drive** - Non indexées, accès contrôlé
2. **Mot de passe dashboard** - Authentification utilisateur
3. **HTTPS/SSL** - Chiffrement des données en transit

## 🛠️ Maintenance

### Mise à jour des Données
1. Remplacer fichiers sur Google Drive
2. Redémarrer l'application Streamlit Cloud
3. Vérifier le bon fonctionnement

### Surveillance
- 📊 Logs d'accès via Streamlit Cloud
- 🔍 Monitoring des erreurs automatique
- 📈 Métriques d'utilisation disponibles

## 📞 Support

### En cas de problème
1. **Données non chargées** : Vérifier les URLs Google Drive
2. **Erreur authentification** : Vérifier les secrets
3. **Erreur déploiement** : Consulter les logs Streamlit Cloud

### Contact
- **Dashboard** : PREVENT Program Analysis
- **Organisation** : CEVA - Gates Foundation
- **Support** : Contactez l'administrateur
- **Sécurité** : Niveau Enterprise

## 🎯 Accès

**URL** : `https://prevent-dashboard-gates.streamlit.app`
**Mot de passe** : Contactez l'administrateur

⚠️ **Confidentiel** - Partager uniquement avec les personnes autorisées