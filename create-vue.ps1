$projectName = "new-energy-carport"
$features = @("TypeScript", "Router", "Pinia", "ESLint")

$inputLines = @($projectName) + @("") * $features.Count + @("")

$inputLines | npm create vue@latest .