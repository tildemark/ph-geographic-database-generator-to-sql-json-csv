import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";
import { ArrowLeft, BookOpen, Code, Database, Download, Layers, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { GeographicSelect } from "@/components/GeographicSelect";
import { SnippetSwitcher } from "@/components/SnippetSwitcher";

export default function DocsPage() {
    return (
        <div className="min-h-screen bg-background pb-20">
            {/* Header */}
            <div className="bg-primary/5 border-b border-primary/10 py-12 px-6 mb-10">
                <div className="container mx-auto max-w-5xl">
                    <Link href="/">
                        <Button variant="ghost" className="gap-2 mb-6 hover:bg-primary/10 transition-colors">
                            <ArrowLeft className="h-4 w-4" /> Back to Home
                        </Button>
                    </Link>
                    <div className="space-y-4">
                        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight">Documentation Guide</h1>
                        <p className="text-xl text-muted-foreground max-w-2xl">
                            A comprehensive guide to understanding Philippine geographic data, ingestion workflows, and API usage.
                        </p>
                    </div>
                </div>
            </div>

            <div className="container mx-auto max-w-5xl px-6 grid grid-cols-1 lg:grid-cols-3 gap-12">

                {/* Main Content */}
                <div className="lg:col-span-2 space-y-16">

                    {/* Interactive Demo */}
                    <section id="demo" className="space-y-6 scroll-mt-20">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-primary/10 rounded-lg text-primary">
                                <BookOpen className="h-6 w-6" />
                            </div>
                            <h2 className="text-2xl font-bold">Interactive Demo</h2>
                        </div>
                        <p className="text-muted-foreground">
                            Test the cascading data retrieval system. Select a region to drill down all the way to the barangay level.
                        </p>
                        <GeographicSelect />
                    </section>

                    {/* Coding Structure */}
                    <section id="structure" className="space-y-6 scroll-mt-20">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-primary/10 rounded-lg text-primary">
                                <Layers className="h-6 w-6" />
                            </div>
                            <h2 className="text-2xl font-bold">10-Digit PSGC Structure</h2>
                        </div>
                        <p className="text-muted-foreground">
                            The system follows the <strong>2024 Revision 1</strong> of the Philippine Standard Geographic Code (PSGC).
                            All codes are consistently padded to 10 digits to ensure compatibility across all levels.
                        </p>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {[
                                { level: "Region", format: "RR00000000", desc: "2-digit Region + 8 Zeros" },
                                { level: "Province/District", format: "RRPRO00000", desc: "2-digit Reg + 3-digit Prov + 5 Zeros" },
                                { level: "City/Municipality", format: "RRPROCM000", desc: "Reg/Prov + 2-digit City + 3 Zeros" },
                                { level: "Barangay", format: "RRPROCMBRG", desc: "Full 10-digit unique identifier" },
                            ].map((item) => (
                                <Card key={item.level} className="border-primary/10">
                                    <CardHeader className="pb-2">
                                        <CardTitle className="text-sm font-bold text-primary active:scale-95 transition-transform">{item.level}</CardTitle>
                                    </CardHeader>
                                    <CardContent>
                                        <code className="text-lg font-mono font-bold">{item.format}</code>
                                        <p className="text-xs text-muted-foreground mt-1">{item.desc}</p>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>
                    </section>

                    {/* Data Sourcing */}
                    <section id="sourcing" className="space-y-6 scroll-mt-20">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-primary/10 rounded-lg text-primary">
                                <Download className="h-6 w-6" />
                            </div>
                            <h2 className="text-2xl font-bold">Sourcing the Data</h2>
                        </div>
                        <p className="text-muted-foreground">
                            To update the dataset, you must obtain the official files from the Philippine Statistics Authority (PSA).
                        </p>
                        <ol className="list-decimal pl-6 space-y-4">
                            <li>Visit the <a href="https://psa.gov.ph/classification/psgc" target="_blank" rel="noopener noreferrer" className="text-primary font-semibold underline underline-offset-4">PSA PSGC Portal</a>.</li>
                            <li>Download the latest <strong>PSGC Publication (Excel)</strong> file.</li>
                            <li>Ensure the file contains the <code>PSGC</code> sheet with the 10-digit coding columns.</li>
                        </ol>
                    </section>

                    {/* Ingestion Workflow */}
                    <section id="ingestion" className="space-y-6 scroll-mt-20">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-primary/10 rounded-lg text-primary">
                                <Database className="h-6 w-6" />
                            </div>
                            <h2 className="text-2xl font-bold">Ingestion Workflow</h2>
                        </div>
                        <div className="space-y-4">
                            <Card className="border-dashed">
                                <CardContent className="p-6 flex items-start gap-4">
                                    <ShieldCheck className="h-6 w-6 text-green-500 mt-1" />
                                    <div>
                                        <h3 className="font-bold">Verified Admin Upload</h3>
                                        <p className="text-sm text-muted-foreground">
                                            The backend features a resilient ingestion engine that automatically identifies columns, cleans messy data,
                                            and performs safe atomic upserts to prevent database corruption.
                                        </p>
                                    </div>
                                </CardContent>
                            </Card>
                            <p className="text-muted-foreground">
                                Whenever a new file is uploaded via the <code>/admin</code> dashboard:
                            </p>
                            <ul className="list-disc pl-6 space-y-2">
                                <li>The database is updated with the latest codes and names.</li>
                                <li>The Redis cache is automatically flushed to ensure fresh data.</li>
                                <li>Static SQL, CSV, and JSON dumps are regenerated for direct download.</li>
                            </ul>
                        </div>
                    </section>

                    {/* Integration section */}
                    <section id="integrate" className="space-y-6 scroll-mt-20">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-primary/10 rounded-lg text-primary">
                                <Code className="h-6 w-6" />
                            </div>
                            <h2 className="text-2xl font-bold">Integrate into your Project</h2>
                        </div>
                        <p className="text-muted-foreground">
                            Ready to use the Geographic API in your application? Use the snippets below to get started quickly with your favorite language or tool.
                        </p>
                        <SnippetSwitcher />
                    </section>

                </div>

                {/* Sidebar Navigation */}
                <aside className="hidden lg:block">
                    <div className="sticky top-10 space-y-6 px-4 py-8 bg-secondary/30 rounded-2xl border border-secondary">
                        <h4 className="font-bold text-sm uppercase tracking-wider text-muted-foreground">On this page</h4>
                        <nav className="flex flex-col gap-3">
                            <a href="#demo" className="text-sm font-medium hover:text-primary transition-colors">Interactive Demo</a>
                            <a href="#structure" className="text-sm font-medium hover:text-primary transition-colors">10-Digit Structure</a>
                            <a href="#sourcing" className="text-sm font-medium hover:text-primary transition-colors">Sourcing the Data</a>
                            <a href="#ingestion" className="text-sm font-medium hover:text-primary transition-colors">Ingestion Workflow</a>
                            <a href="#integrate" className="text-sm font-medium hover:text-primary transition-colors">Integrate into your Project</a>
                        </nav>
                        <div className="pt-6 border-t border-secondary">
                            <Link href="/">
                                <Button className="w-full">Get Started</Button>
                            </Link>
                        </div>
                    </div>
                </aside>
            </div>
        </div>
    );
}
