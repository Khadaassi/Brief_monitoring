Que fait `histogram_quantile()` ?

* réponse:
  Calcule un quantile (ex: P95) à partir d’un histogramme Prometheus (les séries `*_bucket`). En pratique, tu l’utilises avec un `rate()` sur les buckets, puis `histogram_quantile(q, …)` estime la latence/valeur sous laquelle se trouvent q% des observations sur la fenêtre choisie.
  Exemple (P95 latence HTTP) :
  `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`

Quelle est la différence entre `rate()` et `increase()` ?

* réponse:
* `rate(metric[5m])` : renvoie une **vitesse moyenne par seconde** (ex: req/s) sur la fenêtre. Principalement pour **Counters**.
* `increase(metric[5m])` : renvoie **l’augmentation totale** sur la fenêtre (ex: nombre de requêtes sur 5 min).
  Lien simple : `increase(x[5m]) ≈ rate(x[5m]) * 300` (300 secondes).
  Les deux gèrent les resets de counter (redémarrage).

Comment filtrer des métriques par label ?

* réponse:
  Avec un sélecteur `{label="valeur"}` ou `{label=~"regex"}` dans PromQL.
  Exemples :
* `http_requests_total{method="GET", status="200"}`
* `http_requests_total{status=~"5.."}` (toutes les 5xx)
* Exclure : `http_requests_total{handler!="/metrics"}`
  Tu peux aussi agréger ensuite : `sum(rate(http_requests_total{status=~"5.."}[5m])) by (handler)`

Comment nommer correctement une métrique ?

* réponse:
  Règles de base (style Prometheus) :
* **snake_case**, en anglais, descriptif.
* Inclure l’unité en suffixe quand c’est une mesure :

  * temps → `_seconds` (ex: `http_request_duration_seconds`)
  * octets → `_bytes` (ex: `memory_usage_bytes`)
  * total (compteur) → `_total` (ex: `http_requests_total`)
* Préfixer par le domaine si utile : `db_…`, `app_…`, `items_…`
* Pas de label pour encoder une unité (l’unité doit être dans le nom).

Quand utiliser des labels vs créer plusieurs métriques ?

* réponse:
  Utilise des **labels** quand tu veux découper une même mesure en dimensions naturelles et contrôlées (ex: `method`, `status`, `handler`) :
* Bonne idée : `http_requests_total{method="GET", status="200", handler="/items"}`

Crée **plusieurs métriques** quand :

* La mesure n’est pas la même (sémantique différente)
* Les labels risquent d’exploser (trop de valeurs possibles = cardinalité élevée)
* Tu serais tenté de mettre un label unique par user/id/commande → à éviter

Règle pratique : labels = faible cardinalité et stable. Pas de labels avec `user_id`, `email`, `request_id`, etc.

Quels sont les dashboards anti-patterns à éviter ?

* réponse:
* Trop de panels / “mur de graphes” : illisible, personne ne l’utilise.
* Mauvaises unités (ms vs s, % vs ratio), ou pas d’unités.
* Utiliser des métriques brutes de Counter sans `rate()`/`increase()` (ça donne des courbes trompeuses).
* Mettre des labels à forte cardinalité dans les panels (explose Grafana/Prometheus).
* Pas de seuils / pas de contexte (ex: “latence” sans P95/P99 ni objectifs).
* Panels non actionnables (beau mais ne répond pas à “est-ce que ça va ?” et “où est le problème ?”).
* Mélanger des échelles incomparables sur un même graphe sans logique.
* Time range/interval mal réglés (trop zoomé → bruit, trop large → tout est lissé).
