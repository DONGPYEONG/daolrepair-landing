# Extract reviews using .NET JSON parsing
$baseDir = "c:\Users\다올리페어\Downloads\landingpage-20260326T082547Z-3-001\landingpage"

Add-Type -AssemblyName System.Web.Extensions

function Read-FileUtf8($filePath) {
    $stream = [System.IO.File]::Open($filePath, 'Open', 'Read', 'Read')
    $reader = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8)
    $content = $reader.ReadToEnd()
    $reader.Close()
    $stream.Close()
    return $content
}

function Parse-JsonDict($content) {
    $ser = New-Object System.Web.Script.Serialization.JavaScriptSerializer
    $ser.MaxJsonLength = 20000000
    return $ser.Deserialize($content, [System.Collections.Generic.Dictionary[string,object]])
}

function Get-ReviewList($filePath) {
    $content = Read-FileUtf8 $filePath
    $data = Parse-JsonDict $content

    if ($data.ContainsKey('list')) {
        $list = $data['list']
        Write-Host "Found $($list.Count) reviews in $filePath"
        return $list
    }
    Write-Host "No 'list' key. Keys: $($data.Keys -join ', ')"
    return $null
}

function Esc($s) {
    if ($null -eq $s) { return '' }
    $str = $s.ToString()
    $str = $str.Replace('\','\\')
    $str = $str.Replace("'","\'")
    return $str
}

function Get-DictVal($obj, $key) {
    if ($null -eq $obj) { return $null }
    if ($obj -is [System.Collections.Generic.Dictionary[string,object]]) {
        if ($obj.ContainsKey($key)) { return $obj[$key] }
    }
    return $null
}

$all = [System.Collections.ArrayList]::new()
$r1 = Get-ReviewList "$baseDir\reviews_page1.json"
$r2 = Get-ReviewList "$baseDir\reviews_page2.json"

if ($null -ne $r1) { foreach ($item in $r1) { [void]$all.Add($item) } }
if ($null -ne $r2) { foreach ($item in $r2) { [void]$all.Add($item) } }

Write-Host "Total reviews: $($all.Count)"

# Sort by id descending
$sorted = $all | Sort-Object {
    $idVal = Get-DictVal $_ 'id'
    if ($null -ne $idVal) { [int]$idVal } else { 0 }
} -Descending

$lines = [System.Collections.ArrayList]::new()
foreach ($r in $sorted) {
    $id = Get-DictVal $r 'id'
    if ($null -eq $id) { $id = '' }

    $w = Esc(Get-DictVal $r 'writer')
    $t = Esc(Get-DictVal $r 'title')
    $d = Esc(Get-DictVal $r 'seoDescription')

    $dateRaw = Get-DictVal $r 'createdDate'
    $date = ''
    if ($null -ne $dateRaw) {
        $ds = $dateRaw.ToString()
        if ($ds.Length -ge 10) { $date = $ds.Substring(0,10) } else { $date = $ds }
    }

    $img = ''
    $thumb = Get-DictVal $r 'thumbnailImage'
    if ($null -ne $thumb) {
        if ($thumb -is [System.Collections.Generic.Dictionary[string,object]]) {
            $u = Get-DictVal $thumb 'url'
            if ($null -ne $u) { $img = Esc($u) }
        } elseif ($thumb -is [string]) {
            $img = Esc($thumb)
        }
    }

    [void]$lines.Add("  {id:$id,w:'$w',t:'$t',d:'$d',date:'$date',img:'$img'}")
}

$nl = [Environment]::NewLine
$output = "var REVIEWS = [$nl" + ($lines -join (",$nl")) + "$nl];"

# Write using StreamWriter to handle Korean path
$outPath = "$baseDir\reviews_output.js"
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
$stream = New-Object System.IO.FileStream($outPath, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write)
$writer = New-Object System.IO.StreamWriter($stream, $utf8NoBom)
$writer.Write($output)
$writer.Close()
$stream.Close()

Write-Host "Written $($lines.Count) reviews to reviews_output.js"
