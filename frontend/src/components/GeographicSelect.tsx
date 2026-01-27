"use client";

import React, { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Label } from "./ui/label";
import { Loader2, RefreshCw } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface GeoItem {
    code: string;
    name: string;
}

export function GeographicSelect() {
    const [regions, setRegions] = useState<GeoItem[]>([]);
    const [provinces, setProvinces] = useState<GeoItem[]>([]);
    const [cities, setCities] = useState<GeoItem[]>([]);
    const [barangays, setBarangays] = useState<GeoItem[]>([]);

    const [selectedRegion, setSelectedRegion] = useState("");
    const [selectedProvince, setSelectedProvince] = useState("");
    const [selectedCity, setSelectedCity] = useState("");
    const [selectedBarangay, setSelectedBarangay] = useState("");

    const [loading, setLoading] = useState({
        regions: false,
        provinces: false,
        cities: false,
        barangays: false,
    });

    // Fetch Regions on mount
    useEffect(() => {
        fetchRegions();
    }, []);

    const fetchRegions = async () => {
        setLoading((prev) => ({ ...prev, regions: true }));
        try {
            const res = await fetch(`${API_URL}/api/regions`);
            const data = await res.json();
            setRegions(data);
        } catch (error) {
            console.error("Failed to fetch regions:", error);
        } finally {
            setLoading((prev) => ({ ...prev, regions: false }));
        }
    };

    const fetchProvinces = async (regionCode: string) => {
        setLoading((prev) => ({ ...prev, provinces: true }));
        try {
            const res = await fetch(`${API_URL}/api/regions/${regionCode}/provinces`);
            const data = await res.json();
            setProvinces(data);
        } catch (error) {
            console.error("Failed to fetch provinces:", error);
        } finally {
            setLoading((prev) => ({ ...prev, provinces: false }));
        }
    };

    const fetchCities = async (provinceCode: string) => {
        setLoading((prev) => ({ ...prev, cities: true }));
        try {
            const res = await fetch(`${API_URL}/api/provinces/${provinceCode}/cities`);
            const data = await res.json();
            const sortedCities = data.sort((a: any, b: any) => a.name.localeCompare(b.name));
            setCities(sortedCities);
        } catch (error) {
            console.error("Failed to fetch cities:", error);
        } finally {
            setLoading((prev) => ({ ...prev, cities: false }));
        }
    };

    const fetchBarangays = async (cityCode: string) => {
        setLoading((prev) => ({ ...prev, barangays: true }));
        try {
            const res = await fetch(`${API_URL}/api/cities/${cityCode}/barangays`);
            const data = await res.json();
            setBarangays(data);
        } catch (error) {
            console.error("Failed to fetch barangays:", error);
        } finally {
            setLoading((prev) => ({ ...prev, barangays: false }));
        }
    };

    const handleRegionChange = async (e: React.ChangeEvent<HTMLSelectElement>) => {
        const code = e.target.value;
        setSelectedRegion(code);
        setSelectedProvince("");
        setSelectedCity("");
        setSelectedBarangay("");
        setProvinces([]);
        setCities([]);
        setBarangays([]);

        if (code) {
            setLoading((prev) => ({ ...prev, provinces: true }));
            try {
                const res = await fetch(`${API_URL}/api/regions/${code}/provinces`);
                const data = await res.json();

                // Sort for better UX
                const sortedProvinces = data.sort((a: any, b: any) => a.name.localeCompare(b.name));
                setProvinces(sortedProvinces);

                // If region has no provinces (like NCR), fetch cities directly
                if (data.length === 0) {
                    await fetchCitiesByRegion(code);
                }
            } catch (error) {
                console.error("Failed to fetch provinces:", error);
            } finally {
                setLoading((prev) => ({ ...prev, provinces: false }));
            }
        }
    };

    const fetchCitiesByRegion = async (regionCode: string) => {
        setLoading((prev) => ({ ...prev, cities: true }));
        try {
            const res = await fetch(`${API_URL}/api/regions/${regionCode}/cities`);
            const data = await res.json();
            const sortedCities = data.sort((a: any, b: any) => a.name.localeCompare(b.name));
            setCities(sortedCities);
        } catch (error) {
            console.error("Failed to fetch cities by region:", error);
        } finally {
            setLoading((prev) => ({ ...prev, cities: false }));
        }
    };

    const handleProvinceChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const code = e.target.value;
        setSelectedProvince(code);
        setSelectedCity("");
        setSelectedBarangay("");
        setCities([]);
        setBarangays([]);
        if (code) fetchCities(code);
    };

    const handleCityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const code = e.target.value;
        setSelectedCity(code);
        setSelectedBarangay("");
        setBarangays([]);
        if (code) fetchBarangays(code);
    };

    const handleReset = () => {
        setSelectedRegion("");
        setSelectedProvince("");
        setSelectedCity("");
        setSelectedBarangay("");
        setProvinces([]);
        setCities([]);
        setBarangays([]);
    };

    return (
        <Card className="w-full border-2 border-primary/10 shadow-xl overflow-hidden">
            <CardHeader className="bg-primary/5 border-b border-primary/10 py-4">
                <CardTitle className="text-xl font-bold flex items-center gap-2">
                    Sample Form
                </CardTitle>
            </CardHeader>
            <CardContent className="p-6 space-y-6">
                {/* Region */}
                <div className="space-y-2 group">
                    <Label className="text-sm font-semibold text-foreground/70 group-focus-within:text-primary transition-colors">
                        Select Region:
                    </Label>
                    <div className="relative">
                        <select
                            value={selectedRegion}
                            onChange={handleRegionChange}
                            disabled={loading.regions}
                            className="w-full bg-background border-2 border-muted hover:border-primary/50 focus:border-primary focus:ring-4 focus:ring-primary/10 outline-none rounded-xl py-3 px-4 transition-all appearance-none disabled:opacity-50"
                        >
                            <option value="">-- Select Region --</option>
                            {regions.map((r) => (
                                <option key={r.code} value={r.code}>
                                    {r.name}
                                </option>
                            ))}
                        </select>
                        {loading.regions && (
                            <Loader2 className="absolute right-3 top-3.5 h-5 w-5 animate-spin text-primary" />
                        )}
                        {!loading.regions && (
                            <div className="absolute right-4 top-4 pointer-events-none">
                                <svg className="w-4 h-4 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                                </svg>
                            </div>
                        )}
                    </div>
                </div>

                {/* Province */}
                {selectedRegion && provinces.length > 0 && (
                    <div className="space-y-2 group">
                        <Label className="text-sm font-semibold text-foreground/70 group-focus-within:text-primary transition-colors">
                            Select Province:
                        </Label>
                        <div className="relative">
                            <select
                                value={selectedProvince}
                                onChange={handleProvinceChange}
                                disabled={loading.provinces}
                                className="w-full bg-background border-2 border-muted hover:border-primary/50 focus:border-primary focus:ring-4 focus:ring-primary/10 outline-none rounded-xl py-3 px-4 transition-all appearance-none disabled:opacity-50"
                            >
                                <option value="">-- Select Province --</option>
                                {provinces.map((p) => (
                                    <option key={p.code} value={p.code}>
                                        {p.name}
                                    </option>
                                ))}
                            </select>
                            {loading.provinces && (
                                <Loader2 className="absolute right-3 top-3.5 h-5 w-5 animate-spin text-primary" />
                            )}
                            {!loading.provinces && (
                                <div className="absolute right-4 top-4 pointer-events-none">
                                    <svg className="w-4 h-4 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                                    </svg>
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {/* City */}
                {(selectedProvince || cities.length > 0) && (
                    <div className="space-y-2 group">
                        <Label className="text-sm font-semibold text-foreground/70 group-focus-within:text-primary transition-colors">
                            Select City/Municipality:
                        </Label>
                        <div className="relative">
                            <select
                                value={selectedCity}
                                onChange={handleCityChange}
                                disabled={loading.cities || cities.length === 0}
                                className="w-full bg-background border-2 border-muted hover:border-primary/50 focus:border-primary focus:ring-4 focus:ring-primary/10 outline-none rounded-xl py-3 px-4 transition-all appearance-none disabled:opacity-50"
                            >
                                <option value="">-- Select City --</option>
                                {cities.map((c) => (
                                    <option key={c.code} value={c.code}>
                                        {c.name}
                                    </option>
                                ))}
                            </select>
                            {loading.cities && (
                                <Loader2 className="absolute right-3 top-3.5 h-5 w-5 animate-spin text-primary" />
                            )}
                            {!loading.cities && (
                                <div className="absolute right-4 top-4 pointer-events-none">
                                    <svg className="w-4 h-4 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                                    </svg>
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {/* Barangay */}
                {(selectedCity || barangays.length > 0) && (
                    <div className="space-y-2 group">
                        <Label className="text-sm font-semibold text-foreground/70 group-focus-within:text-primary transition-colors">
                            Select Barangay:
                        </Label>
                        <div className="relative">
                            <select
                                value={selectedBarangay}
                                onChange={(e) => setSelectedBarangay(e.target.value)}
                                disabled={loading.barangays || barangays.length === 0}
                                className="w-full bg-background border-2 border-muted hover:border-primary/50 focus:border-primary focus:ring-4 focus:ring-primary/10 outline-none rounded-xl py-3 px-4 transition-all appearance-none disabled:opacity-50"
                            >
                                <option value="">-- Select Barangay --</option>
                                {barangays.map((b) => (
                                    <option key={b.code} value={b.code}>
                                        {b.name}
                                    </option>
                                ))}
                            </select>
                            {loading.barangays && (
                                <Loader2 className="absolute right-3 top-3.5 h-5 w-5 animate-spin text-primary" />
                            )}
                            {!loading.barangays && (
                                <div className="absolute right-4 top-4 pointer-events-none">
                                    <svg className="w-4 h-4 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                                    </svg>
                                </div>
                            )}
                        </div>
                    </div>
                )}

                <Button
                    onClick={handleReset}
                    variant="destructive"
                    className="w-full h-12 text-lg font-bold rounded-xl shadow-lg shadow-destructive/20 hover:scale-[1.02] active:scale-[0.98] transition-all gap-2"
                >
                    <RefreshCw className="h-5 w-5" /> Reset
                </Button>

                {/* PSGC Code Display */}
                {selectedRegion && (
                    <div className="mt-4 p-4 bg-primary/10 rounded-xl border border-primary/20 animate-in fade-in slide-in-from-top-2">
                        <p className="text-sm font-medium text-primary mb-3">Selected PSGC Codes:</p>
                        <div className="space-y-2">
                            {/* Region Code */}
                            <div className="flex items-start gap-3">
                                <div className="flex-shrink-0 w-24 text-xs font-semibold text-primary/70">
                                    Region:
                                </div>
                                <div className="flex-1">
                                    <span className="font-mono font-bold text-lg">{selectedRegion}</span>
                                    <span className="ml-2 text-sm text-muted-foreground">
                                        ({regions.find(r => r.code === selectedRegion)?.name})
                                    </span>
                                </div>
                            </div>

                            {/* Province Code */}
                            {selectedProvince && (
                                <div className="flex items-start gap-3">
                                    <div className="flex-shrink-0 w-24 text-xs font-semibold text-primary/70">
                                        Province:
                                    </div>
                                    <div className="flex-1">
                                        <span className="font-mono font-bold text-lg">{selectedProvince}</span>
                                        <span className="ml-2 text-sm text-muted-foreground">
                                            ({provinces.find(p => p.code === selectedProvince)?.name})
                                        </span>
                                    </div>
                                </div>
                            )}

                            {/* City Code */}
                            {selectedCity && (
                                <div className="flex items-start gap-3">
                                    <div className="flex-shrink-0 w-24 text-xs font-semibold text-primary/70">
                                        City:
                                    </div>
                                    <div className="flex-1">
                                        <span className="font-mono font-bold text-lg">{selectedCity}</span>
                                        <span className="ml-2 text-sm text-muted-foreground">
                                            ({cities.find(c => c.code === selectedCity)?.name})
                                        </span>
                                    </div>
                                </div>
                            )}

                            {/* Barangay Code */}
                            {selectedBarangay && (
                                <div className="flex items-start gap-3">
                                    <div className="flex-shrink-0 w-24 text-xs font-semibold text-primary/70">
                                        Barangay:
                                    </div>
                                    <div className="flex-1">
                                        <span className="font-mono font-bold text-lg">{selectedBarangay}</span>
                                        <span className="ml-2 text-sm text-muted-foreground">
                                            ({barangays.find(b => b.code === selectedBarangay)?.name})
                                        </span>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </CardContent>
        </Card>
    );
}
