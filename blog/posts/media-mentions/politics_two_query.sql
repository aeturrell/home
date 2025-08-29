SELECT 
  EXTRACT(YEAR FROM PARSE_DATETIME('%Y%m%d%H%M%S', CAST(DATE AS STRING))) as Year,
  EXTRACT(MONTH FROM PARSE_DATETIME('%Y%m%d%H%M%S', CAST(DATE AS STRING))) as Month,
  REGEXP_EXTRACT(DocumentIdentifier, r'^(https?://[^/]+)') as Truncated_URL,
  CASE 
    WHEN REGEXP_CONTAINS(Persons, r'(?i)nigel.farage') THEN 'Nigel Farage'
    WHEN REGEXP_CONTAINS(Persons, r'(?i)ed.davey') THEN 'Ed Davey'
    WHEN REGEXP_CONTAINS(Persons, r'(?i)kemi.badenoch') THEN 'Kemi Badenoch'
  END as Person_Mentioned,
  COUNT(*) as Mentions
FROM `gdelt-bq.gdeltv2.gkg_partitioned`
WHERE 
  DATE >= 20240101000000  -- Adjust date range as needed
  AND DocumentIdentifier IS NOT NULL
  AND (
    REGEXP_CONTAINS(Persons, r'(?i)nigel.farage') OR
    REGEXP_CONTAINS(Persons, r'(?i)ed.davey') OR
    REGEXP_CONTAINS(Persons, r'(?i)kemi.badenoch')
  )
GROUP BY Year, Month, Truncated_URL, Person_Mentioned
ORDER BY Year DESC, Month DESC, Mentions DESC, Truncated_URL
