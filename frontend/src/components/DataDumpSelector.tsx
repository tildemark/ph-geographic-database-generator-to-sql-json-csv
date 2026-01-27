"use client";

import React, { useState } from "react";
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Download, FileJson, FileType, FileCode, Code } from "lucide-react";

type DataFormat = "json" | "csv" | "sql" | "xml";

interface DumpCategory {
    id: string;
    label: string;
    description: string;
}

export function DataDumpSelector() {
    const [selectedFormat, setSelectedFormat] = useState<DataFormat>("json");

    const formats: { id: DataFormat; label: string; icon: React.ReactNode }[] = [
        { id: "json", label: "JSON", icon: <FileJson className="h-4 w-4" /> },
        { id: "csv", label: "CSV", icon: <FileType className="h-4 w-4" /> },
        { id: "sql", label: "SQL", icon: <FileCode className="h-4 w-4" /> },
        { id: "xml", label: "XML", icon: <Code className="h-4 w-4" /> },
    ];

    const categories: DumpCategory[] = [
        { id: "all", label: "Complete Dataset", description: "All regions, provinces, cities, and barangays" },
        { id: "regions", label: "Regions Only", description: "All Philippine regions" },
        { id: "provinces", label: "Provinces Only", description: "All provinces and districts" },
        { id: "cities", label: "Cities & Municipalities", description: "All cities and municipalities" },
        { id: "barangays", label: "Barangays", description: "All barangays nationwide" },
    ];

    const getDownloadUrl = (category: string, format: DataFormat) => {
        return `/downloads/${category}.${format}`;
    };

    return (
        <div className="space-y-6">
            {/* Format Selector */}
            <div>
                <h3 className="text-sm font-semibold text-muted-foreground mb-3">Select Format:</h3>
                <div className="flex flex-wrap gap-2">
                    {formats.map((format) => (
                        <Button
                            key={format.id}
                            variant={selectedFormat === format.id ? "default" : "outline"}
                            onClick={() => setSelectedFormat(format.id)}
                            className="flex items-center gap-2 rounded-lg transition-all"
                        >
                            {format.icon}
                            {format.label}
                        </Button>
                    ))}
                </div>
            </div>

            {/* Download Categories */}
            <div className="space-y-3">
                <h3 className="text-sm font-semibold text-muted-foreground">Available Downloads:</h3>
                <div className="grid grid-cols-1 gap-3">
                    {categories.map((category) => (
                        <Card key={category.id} className="border-primary/10 hover:border-primary/30 transition-colors">
                            <CardContent className="p-4 flex items-center justify-between">
                                <div className="flex-1">
                                    <h4 className="font-semibold text-sm">{category.label}</h4>
                                    <p className="text-xs text-muted-foreground mt-0.5">{category.description}</p>
                                </div>
                                <Button
                                    size="sm"
                                    variant="secondary"
                                    className="gap-2 ml-4"
                                    asChild
                                >
                                    <a
                                        href={getDownloadUrl(category.id, selectedFormat)}
                                        download
                                        className="flex items-center gap-2"
                                    >
                                        <Download className="h-3.5 w-3.5" />
                                        Download
                                    </a>
                                </Button>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>

            {/* Format Info */}
            <Card className="border-dashed bg-secondary/20">
                <CardContent className="p-4">
                    <p className="text-xs text-muted-foreground">
                        <strong>Note:</strong> All dumps are generated automatically during data ingestion.
                        Files are updated whenever new PSGC data is uploaded via the Admin dashboard.
                    </p>
                </CardContent>
            </Card>
        </div>
    );
}
