import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function DocsPage() {
    return (
        <div className="min-h-screen bg-background py-10 px-6">
            <div className="container mx-auto max-w-4xl space-y-8">

                <Link href="/">
                    <Button variant="ghost" className="gap-2 mb-4">
                        <ArrowLeft className="h-4 w-4" /> Back to Home
                    </Button>
                </Link>

                <div className="space-y-2">
                    <h1 className="text-3xl font-bold">Documentation Guide</h1>
                    <p className="text-muted-foreground">How to use the Data and API</p>
                </div>

                <section className="space-y-4">
                    <h2 className="text-xl font-semibold">1. Data Structure</h2>
                    <p>The data fits the PSA's standard hierarchy:</p>
                    <ul className="list-disc pl-6 space-y-2">
                        <li><strong>Region</strong>: The highest level (e.g., NCR, Region III).</li>
                        <li><strong>Province</strong>: Major subdivisions (e.g., Bulacan, Cebu). NCR has Districts.</li>
                        <li><strong>City/Municipality</strong>: Cities (HUC, Component) and Municipalities.</li>
                        <li><strong>Barangay</strong>: The smallest political unit.</li>
                    </ul>
                </section>

                <section className="space-y-4">
                    <h2 className="text-xl font-semibold">2. Using the API</h2>
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-base">Listing Regions</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <pre className="bg-secondary p-4 rounded-md overflow-x-auto">
                                GET /api/regions
                            </pre>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle className="text-base">Drilling Down</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-2">
                            <p className="text-sm">Use the PSGC code from the parent to fetch children.</p>
                            <pre className="bg-secondary p-4 rounded-md overflow-x-auto">
                                GET /api/regions/&#123;region_code&#125;/provinces
                            </pre>
                            <pre className="bg-secondary p-4 rounded-md overflow-x-auto">
                                GET /api/provinces/&#123;province_code&#125;/cities
                            </pre>
                        </CardContent>
                    </Card>
                </section>

                <section className="space-y-4">
                    <h2 className="text-xl font-semibold">3. Static Dumps</h2>
                    <p>
                        The system automatically generates static JSON and CSV files whenever the database is updated.
                        You can download these from the home page.
                    </p>
                </section>
            </div>
        </div>
    );
}
