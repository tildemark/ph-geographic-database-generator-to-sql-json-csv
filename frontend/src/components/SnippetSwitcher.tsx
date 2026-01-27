"use client";

import React, { useState } from "react";
import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";
import { Terminal, Globe, Code, Coffee, Check, Copy } from "lucide-react";

interface Snippet {
    id: string;
    label: string;
    icon: React.ReactNode;
    lang: string;
    code: string;
}

export function SnippetSwitcher() {
    const [activeTab, setActiveTab] = useState("curl");
    const [copied, setCopied] = useState(false);

    const snippets: Snippet[] = [
        {
            id: "curl",
            label: "cURL",
            icon: <Terminal className="h-4 w-4" />,
            lang: "bash",
            code: `curl -X GET "http://localhost:8000/api/regions/0300000000/provinces" \\
     -H "Accept: application/json"`,
        },
        {
            id: "js",
            label: "JavaScript",
            icon: <Globe className="h-4 w-4" />,
            lang: "javascript",
            code: `async function fetchProvinces(regionCode) {
  try {
    const res = await fetch(\`http://localhost:8000/api/regions/\${regionCode}/provinces\`);
    const data = await res.json();
    console.log(data);
  } catch (error) {
    console.error("API Error:", error);
  }
}

fetchProvinces("0300000000");`,
        },
        {
            id: "php",
            label: "PHP",
            icon: <Code className="h-4 w-4" />,
            lang: "php",
            code: `<?php
$region_code = "0300000000";
$url = "http://localhost:8000/api/regions/$region_code/provinces";

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, ["Accept: application/json"]);

$response = curl_exec($ch);
curl_close($ch);

$data = json_decode($response, true);
print_r($data);
?>`,
        },
        {
            id: "python",
            label: "Python",
            icon: <Coffee className="h-4 w-4" />,
            lang: "python",
            code: `import requests

def get_provinces(region_code):
    url = f"http://localhost:8000/api/regions/{region_code}/provinces"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(data)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

get_provinces("0300000000")`,
        },
    ];

    const activeSnippet = snippets.find((s) => s.id === activeTab) || snippets[0];

    const handleCopy = () => {
        navigator.clipboard.writeText(activeSnippet.code);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="space-y-4">
            <div className="flex flex-wrap gap-2 overflow-x-auto pb-1 scrollbar-hide">
                {snippets.map((s) => (
                    <Button
                        key={s.id}
                        variant={activeTab === s.id ? "default" : "outline"}
                        onClick={() => setActiveTab(s.id)}
                        className="flex items-center gap-2 rounded-lg transition-all"
                    >
                        {s.icon}
                        {s.label}
                    </Button>
                ))}
            </div>

            <Card className="border-2 border-primary/5 bg-[#0d1117] overflow-hidden shadow-2xl relative">
                <div className="flex items-center justify-between px-4 py-2 bg-white/5 border-b border-white/10">
                    <div className="flex gap-1.5">
                        <div className="w-3 h-3 rounded-full bg-red-500/50" />
                        <div className="w-3 h-3 rounded-full bg-yellow-500/50" />
                        <div className="w-3 h-3 rounded-full bg-green-500/50" />
                    </div>
                    <Button
                        variant="ghost"
                        size="sm"
                        onClick={handleCopy}
                        className="text-gray-400 hover:text-white transition-colors gap-2 h-8"
                    >
                        {copied ? <Check className="h-3.5 w-3.5 text-green-500" /> : <Copy className="h-3.5 w-3.5" />}
                        {copied ? "Copied!" : "Copy"}
                    </Button>
                </div>
                <CardContent className="p-0">
                    <pre className="p-6 text-sm font-mono text-gray-300 overflow-x-auto leading-relaxed selection:bg-primary/30">
                        <code>{activeSnippet.code}</code>
                    </pre>
                </CardContent>
            </Card>
        </div>
    );
}
