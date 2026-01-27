'use client';

import Link from "next/link";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowRight, CheckCircle2, Database, Download, FileJson, FileType, Server } from "lucide-react";
import { DataDumpSelector } from "@/components/DataDumpSelector";

export default function Home() {
  const [apiStatus, setApiStatus] = useState<string>("Checking...");
  const [psgcVersion, setPsgcVersion] = useState<string>("");

  useEffect(() => {
    const checkApi = async () => {
      try {
        const res = await fetch(process.env.NEXT_PUBLIC_API_URL + "/regions");
        if (res.ok) {
          setApiStatus("Online");
        } else {
          setApiStatus("Offline");
        }
      } catch (e) {
        setApiStatus("Offline");
      }
    };

    const fetchMetadata = async () => {
      try {
        const res = await fetch(process.env.NEXT_PUBLIC_API_URL + "/metadata");
        if (res.ok) {
          const data = await res.json();
          if (data.psgc_version) {
            setPsgcVersion(data.psgc_version);
          }
        }
      } catch (e) {
        console.error("Failed to fetch metadata:", e);
      }
    };

    checkApi();
    fetchMetadata();
  }, []);

  return (
    <main className="min-h-screen bg-background flex flex-col">
      {/* Hero Section */}
      <section className="bg-gradient-to-b from-secondary/50 to-background py-20 px-6">
        <div className="container mx-auto max-w-5xl text-center space-y-6">
          <div className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-primary text-primary-foreground hover:bg-primary/80 mb-4">
            {psgcVersion ? `PSGC Data: ${psgcVersion}` : "v2.2.0 Open Source"}
          </div>
          <h1 className="text-4xl md:text-6xl font-bold tracking-tighter">
            Open PH Geographic Data Platform
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            The modern, high-performance source for the Philippine Standard Geographic Code (PSGC).
            Served via fast API and static dumps.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-6">
            <Link href="/docs-guide">
              <Button size="lg" className="gap-2">
                Get Started <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
            <Link href={process.env.NEXT_PUBLIC_API_URL + "/docs"} target="_blank">
              <Button variant="outline" size="lg" className="gap-2">
                API Docs
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Status & Downloads */}
      <section className="py-16 px-6 container mx-auto max-w-5xl">
        <div className="grid md:grid-cols-2 gap-8">

          {/* Live System Status */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Server className="h-5 w-5" /> System Status
              </CardTitle>
              <CardDescription>Real-time availability of the Public API</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between p-4 border rounded-lg bg-secondary/20">
                <span className="font-medium">API Endpoint</span>
                <span className={`flex items-center gap-2 font-bold ${apiStatus === 'Online' ? 'text-green-600' : 'text-red-600'}`}>
                  {apiStatus === 'Online' && <CheckCircle2 className="h-4 w-4" />}
                  {apiStatus}
                </span>
              </div>
              <p className="text-xs text-muted-foreground mt-4">
                Endpoint: {process.env.NEXT_PUBLIC_API_URL}
              </p>
            </CardContent>
          </Card>

          {/* Download Dumps */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="h-5 w-5" /> Data Dumps
              </CardTitle>
              <CardDescription>Static files generated automatically from PSGC data</CardDescription>
            </CardHeader>
            <CardContent>
              <DataDumpSelector />
            </CardContent>
          </Card>

        </div>
      </section>

      <footer className="py-8 text-center text-sm text-muted-foreground border-t mt-auto">
        <p>Open PH Geographic Data Platform • MIT License</p>
      </footer>
    </main>
  );
}
