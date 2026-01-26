'use client';

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Progress } from "@/components/ui/progress";
import { AlertCircle, CheckCircle, Upload } from "lucide-react";

export default function AdminPage() {
    const [secret, setSecret] = useState("");
    const [file, setFile] = useState<File | null>(null);
    const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
    const [message, setMessage] = useState("");

    const handleUpload = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!file || !secret) return;

        setStatus("uploading");

        // The backend expects 'secret' as a query param based on the "Depends" default behavior for scalars
        // But verify_admin logic: secret: str = Depends(verify_admin). verify_admin just checks value.
        // In FastAPI, scalar dependencies are query params by default. 
        // Let's attach it to query string.

        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/upload-psgc?secret=${encodeURIComponent(secret)}`, {
                method: "POST",
                body: formData,
            });

            const data = await res.json();

            if (res.ok) {
                setStatus("success");
                setMessage(data.message || "Upload started successfully.");
            } else {
                setStatus("error");
                setMessage(data.detail || "Upload failed.");
            }
        } catch (err) {
            setStatus("error");
            setMessage("Network error occurred.");
        }
    };

    return (
        <div className="min-h-screen bg-background py-10 px-6 flex justify-center items-center">
            <Card className="w-full max-w-md">
                <CardHeader>
                    <CardTitle>Admin Ingest</CardTitle>
                    <CardDescription>Upload official PSGC Excel file to update database.</CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleUpload} className="space-y-6">

                        <div className="space-y-2">
                            <Label htmlFor="secret">Admin Secret</Label>
                            <Input
                                id="secret"
                                type="password"
                                placeholder="Enter secret key"
                                value={secret}
                                onChange={(e) => setSecret(e.target.value)}
                                required
                            />
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="file">PSGC Excel File</Label>
                            <Input
                                id="file"
                                type="file"
                                accept=".xlsx, .xls"
                                onChange={(e) => setFile(e.target.files?.[0] || null)}
                                required
                            />
                        </div>

                        {status === 'uploading' && (
                            <div className="space-y-2">
                                <Progress value={50} className="w-full animate-pulse" />
                                <p className="text-xs text-center text-muted-foreground">Uploading and processing...</p>
                            </div>
                        )}

                        {status === 'success' && (
                            <div className="p-3 bg-green-50 text-green-700 rounded-md flex items-center gap-2 text-sm border border-green-200">
                                <CheckCircle className="h-4 w-4" /> {message}
                            </div>
                        )}

                        {status === 'error' && (
                            <div className="p-3 bg-red-50 text-red-700 rounded-md flex items-center gap-2 text-sm border border-red-200">
                                <AlertCircle className="h-4 w-4" /> {message}
                            </div>
                        )}

                        <Button type="submit" className="w-full" disabled={status === 'uploading'}>
                            <Upload className="h-4 w-4 mr-2" />
                            {status === 'uploading' ? "Processing..." : "Start Ingest"}
                        </Button>

                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
