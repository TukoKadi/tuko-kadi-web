"use client";

import { useState, useEffect } from "react";
import dynamic from 'next/dynamic';
import registrationDataRaw from "./centers.json";
const registrationData = registrationDataRaw as Record<string, Record<string, any>>;

const OpenMap = dynamic(() => import('../components/Map'), { 
  ssr: false, 
  loading: () => <div className="h-64 bg-gray-100 animate-pulse flex items-center justify-center rounded-xl">Loading Map...</div> 
});

export default function Home() {
  const [county, setCounty] = useState("");
  const [constituency, setConstituency] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [recentSearches, setRecentSearches] = useState<string[]>([]);
  const [showShare, setShowShare] = useState(false);

  const counties = Object.keys(registrationData);
  const filteredCounties = counties.filter(c => 
    c.toLowerCase().includes(searchTerm.toLowerCase())
  );
  const constituencies = county ? Object.keys((registrationData as any)[county]) : [];
  const centerData = (county && constituency) ? (registrationData as any)[county][constituency] : null;

  // Load recent searches
  useEffect(() => {
    const saved = localStorage.getItem("tuko_recent");
    if (saved) setRecentSearches(JSON.parse(saved));
  }, []);

  // Save search
  const saveRecentSearch = (selectedCounty: string, selectedConstituency: string) => {
    const newSearch = `${selectedCounty} - ${selectedConstituency}`;
    const updated = [newSearch, ...recentSearches.filter(s => s !== newSearch)].slice(0, 3);
    setRecentSearches(updated);
    localStorage.setItem("tuko_recent", JSON.stringify(updated));
  };

  const handleCountySelect = (selectedCounty: string) => {
    setCounty(selectedCounty);
    setConstituency("");
  };

  const handleConstituencySelect = (selectedConstituency: string) => {
    setConstituency(selectedConstituency);
    if (county && selectedConstituency) {
      saveRecentSearch(county, selectedConstituency);
    }
  };

  const shareToWhatsApp = () => {
    if (!centerData) return;
    const message = `📍 *TUKO KADI* - IEBC Registration Center\n\nCounty: ${county}\nConstituency: ${constituency}\nCenter: ${centerData.name}\nAddress: ${centerData.address || "Check map"}\nHours: ${centerData.hours || "8am-5pm"}\n\nPowered by Tuko Kadi - Citizen Led`;
    window.open(`https://wa.me/?text=${encodeURIComponent(message)}`, '_blank');
  };

  const copyToClipboard = () => {
    const text = `${centerData?.name}\n${centerData?.address || ""}\n${county} - ${constituency}\nBring your ID. Hours: 8am-5pm`;
    navigator.clipboard.writeText(text);
    alert("Copied to clipboard!");
  };

  return (
    <main className="min-h-screen bg-white text-black p-6 font-sans flex flex-col items-center">
      <div className="max-w-md w-full">
        
        {/* Header Section */}
        <div className="flex justify-between items-start mb-8">
          <div>
            <h1 className="text-4xl font-black tracking-tighter">TUKO KADI</h1>
            <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mt-1">Citizen Led • Open Source</p>
          </div>
          <a href="https://github.com/YOUR_USERNAME/tuko-kadi-web/edit/main/app/centers.json" 
             target="_blank" 
             className="bg-black text-white text-[10px] font-black py-2 px-3 rounded-full hover:bg-gray-800 transition-all uppercase">
            + Add Center
          </a>
        </div>

        {/* Search Input */}
        <div className="mb-4">
          <input
            type="text"
            placeholder="🔍 Search county..."
            className="w-full p-3 bg-gray-50 border border-gray-100 rounded-2xl text-sm outline-none focus:ring-2 focus:ring-black"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        {/* Recent Searches */}
        {recentSearches.length > 0 && !county && (
          <div className="mb-4">
            <p className="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-2">Recent</p>
            <div className="flex gap-2 flex-wrap">
              {recentSearches.map((search, idx) => {
                const [recentCounty, recentConst] = search.split(" - ");
                return (
                  <button
                    key={idx}
                    onClick={() => {
                      setCounty(recentCounty);
                      setConstituency(recentConst);
                      setSearchTerm("");
                    }}
                    className="text-xs bg-gray-100 px-3 py-1.5 rounded-full hover:bg-gray-200"
                  >
                    {search}
                  </button>
                );
              })}
            </div>
          </div>
        )}

        <div className="space-y-4">
          {/* County Select */}
          <select 
            className="w-full p-4 bg-gray-50 border border-gray-100 rounded-2xl font-bold appearance-none outline-none focus:ring-2 focus:ring-black"
            onChange={(e) => handleCountySelect(e.target.value)}
            value={county}
          >
            <option value="">Select County</option>
            {filteredCounties.map(c => <option key={c} value={c}>{c}</option>)}
          </select>

          {/* Constituency Select */}
          {county && (
            <select 
              className="w-full p-4 bg-gray-50 border border-gray-100 rounded-2xl font-bold appearance-none outline-none focus:ring-2 focus:ring-black animate-in fade-in slide-in-from-top-2"
              onChange={(e) => handleConstituencySelect(e.target.value)}
              value={constituency}
            >
              <option value="">Select Constituency</option>
              {constituencies.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          )}

          {/* THE RESULT AREA */}
          {centerData && (
            <div className="mt-8 space-y-4 animate-in zoom-in-95 duration-300">
              <div className="p-6 bg-black text-white rounded-3xl shadow-xl">
                <p className="text-[10px] font-bold opacity-50 uppercase tracking-widest mb-1">Registration Hub</p>
                <h2 className="text-2xl font-black">{centerData.name}</h2>
                {centerData.address && (
                  <p className="text-sm text-gray-300 mt-2">{centerData.address}</p>
                )}
                <div className="mt-4 pt-4 border-t border-white/10 space-y-2">
                  <p className="text-[10px] font-bold text-red-400 tracking-widest uppercase">⚠️ BRING ORIGINAL ID</p>
                  <p className="text-[10px] font-bold text-gray-400 tracking-widest uppercase">🕒 {centerData.hours || "8AM - 5PM"}</p>
                  {centerData.phone && (
                    <p className="text-[10px] font-bold text-gray-400 tracking-widest uppercase">📞 {centerData.phone}</p>
                  )}
                </div>
              </div>

              {/* MAP COMPONENT - With fallback */}
              {centerData.coords ? (
                <div className="rounded-3xl overflow-hidden border border-gray-200 shadow-sm h-64">
                  <OpenMap coordinates={centerData.coords} centerName={centerData.name} />
                </div>
              ) : (
                <div className="p-4 bg-yellow-50 rounded-2xl text-center border border-yellow-200">
                  <p className="text-sm text-yellow-800">📍 {centerData.address || "IEBC Constituency Office"}</p>
                  <a 
                    href={`https://www.google.com/maps/search/${encodeURIComponent(centerData.name + " " + (centerData.address || county + " " + constituency))}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 text-sm underline mt-2 inline-block font-medium"
                  >
                    Get directions on Google Maps →
                  </a>
                </div>
              )}
              
              {/* Share Buttons */}
              <div className="flex gap-2">
                <button 
                  onClick={shareToWhatsApp}
                  className="flex-1 py-3 border-2 border-black rounded-2xl font-black uppercase text-sm hover:bg-black hover:text-white transition-all flex items-center justify-center gap-2"
                >
                  📢 WhatsApp
                </button>
                <button 
                  onClick={copyToClipboard}
                  className="flex-1 py-3 border-2 border-gray-300 rounded-2xl font-bold uppercase text-sm hover:bg-gray-100 transition-all"
                >
                  📋 Copy
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Stats footer */}
        <footer className="mt-16 text-center">
          <p className="text-[10px] text-gray-300 font-bold uppercase tracking-[0.2em]">
            {Object.keys(registrationData).length} Counties • 
            {Object.values(registrationData).reduce((acc, curr) => acc + Object.keys(curr).length, 0)} Constituencies
          </p>
          <p className="text-[10px] text-gray-300 font-bold uppercase tracking-[0.2em] mt-2">Privacy First • For Kenya • 2027</p>
        </footer>
      </div>
    </main>
  );
}
