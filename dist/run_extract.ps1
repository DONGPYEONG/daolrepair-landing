Add-Type -AssemblyName System.Web.Extensions
$ser = New-Object System.Web.Script.Serialization.JavaScriptSerializer
$ser.MaxJsonLength = 20000000

function ReadFile($p) {
    $s = [System.IO.File]::Open($p, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::Read)
    $r = New-Object System.IO.StreamReader($s, [System.Text.Encoding]::UTF8)
    $c = $r.ReadToEnd()
    $r.Close()
    $s.Close()
    return $c
}

function EscStr($s) {
    if ($null -eq $s) { return '' }
    $str = $s.ToString()
    $str = $str -replace '\\', '\\\\'
    $str = $str -replace "'", "\'"
    return $str
}

function GetVal($obj, $key) {
    if ($null -eq $obj) { return $null }
    if ($obj -is [System.Collections.Generic.Dictionary[string,object]]) {
        if ($obj.ContainsKey($key)) { return $obj[$key] }
    }
    return $null
}

$base = $PSScriptRoot

$c1 = ReadFile (Join-Path $base 'reviews_page1.json')
$c2 = ReadFile (Join-Path $base 'reviews_page2.json')

$d1 = $ser.Deserialize($c1, [System.Collections.Generic.Dictionary[string,object]])
$d2 = $ser.Deserialize($c2, [System.Collections.Generic.Dictionary[string,object]])

Write-Host "Page1: $($d1['list'].Count) reviews"
Write-Host "Page2: $($d2['list'].Count) reviews"

$all = [System.Collections.ArrayList]::new()
foreach ($item in $d1['list']) { [void]$all.Add($item) }
foreach ($item in $d2['list']) { [void]$all.Add($item) }

Write-Host "Total: $($all.Count)"

# Build array of [id, item] pairs, sort, then extract
$pairs = @()
foreach ($item in $all) {
    $idv = GetVal $item 'id'
    $idInt = if ($null -ne $idv) { [int]$idv } else { 0 }
    $pairs += ,@($idInt, $item)
}
# Sort pairs by first element descending
$pairs = $pairs | Sort-Object { $_[0] } -Descending
$sorted = @()
foreach ($pair in $pairs) { $sorted += $pair[1] }

$lines = [System.Collections.ArrayList]::new()
foreach ($rv in $sorted) {
    $id = GetVal $rv 'id'
    if ($null -eq $id) { $id = '' }
    $w = EscStr(GetVal $rv 'writer')
    $t = EscStr(GetVal $rv 'title')
    $d = EscStr(GetVal $rv 'seoDescription')
    $dr = GetVal $rv 'createdDate'
    if ($null -ne $dr) {
        $ds = $dr.ToString()
        $date = if ($ds.Length -ge 10) { $ds.Substring(0,10) } else { $ds }
    } else {
        $date = ''
    }
    $img = ''
    $th = GetVal $rv 'thumbnailImage'
    if ($null -ne $th) {
        if ($th -is [System.Collections.Generic.Dictionary[string,object]]) {
            $u = GetVal $th 'url'
            if ($null -ne $u) { $img = EscStr($u) }
        } elseif ($th -is [string]) {
            $img = EscStr($th)
        }
    }
    $line = "  {id:" + $id + ",w:'" + $w + "',t:'" + $t + "',d:'" + $d + "',date:'" + $date + "',img:'" + $img + "'}"
    [void]$lines.Add($line)
}

$nl = [Environment]::NewLine
$output = "var REVIEWS = [" + $nl + ($lines -join ("," + $nl)) + $nl + "];"

$outPath = Join-Path $base 'reviews_output.js'
$enc = New-Object System.Text.UTF8Encoding $false
$fs = New-Object System.IO.FileStream($outPath, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write)
$sw = New-Object System.IO.StreamWriter($fs, $enc)
$sw.Write($output)
$sw.Close()
$fs.Close()

Write-Host "Written $($lines.Count) entries to reviews_output.js"
