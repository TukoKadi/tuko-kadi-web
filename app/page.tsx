"use client";

import { useState } from "react";
import dynamic from 'next/dynamic';
import registrationData from "./centers.json";

// We load the map only on the client side so it doesn't slow down the page
const OpenMap = dynamic(() => import('../components/Map'), { 
  ssr: false, 
  loading: () => <div className="h-64 bg-gray-100 animate-pulse flex items-center justify-center rounded-xl">Loading Map...</div> 
});

export default function Home() {
  const [county, setCounty] = useState("");
  const [constituency, setConstituency] = useState("");

  const counties = Object.keys(registrationData);
  const constituencies = county ? Object.keys((registrationData as any)[county]) : [];
  const centerData = (county && constituency) ? (registrationData as any)[county][constituency] : null;

  return (
    <main className="min-h-screen bg-white text-black p-6 font-sans flex flex-col items-center">
      <div className="max-w-md w-full">
        
        {/* Header Section */}
        <div className="flex justify-between items-start mb-8">
          <div>
            <h1 className="text-4xl font-black tracking-tighter">TUKO KADI</h1>
            <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mt-1">Citizen Led • Open Source</p>
          </div>
          {/* CROWDSOURCE BUTTON - This is how we defeat the "Missing Data" problem */}
          <a href="https://github.com/YOUR_USERNAME/tuko-kadi-web/edit/main/app/centers.json" 
             target="_blank" 
             className="bg-black text-white text-[10px] font-black py-2 px-3 rounded-full hover:bg-gray-800 transition-all uppercase">
            + Add Center
          </a>
        </div>

        <div className="space-y-4">
          {/* County Select */}
          <select className="w-full p-4 bg-gray-50 border border-gray-100 rounded-2xl font-bold appearance-none outline-none focus:ring-2 focus:ring-black"
            onChange={(e) => {setCounty(e.target.value); setConstituency("");}}>
            <option value="">Select County</option>
            {counties.map(c => <option key={c} value={c}>{c}</option>)}
          </select>

          {/* Constituency Select */}
          {county && (
            <select className="w-full p-4 bg-gray-50 border border-gray-100 rounded-2xl font-bold appearance-none outline-none focus:ring-2 focus:ring-black animate-in fade-in slide-in-from-top-2"
              onChange={(e) => setConstituency(e.target.value)}>
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
                <div className="mt-4 pt-4 border-t border-white/10 space-y-2">
                  <p className="text-[10px] font-bold text-red-400 tracking-widest uppercase">⚠️ BRING ORIGINAL ID</p>
                  <p className="text-[10px] font-bold text-gray-400 tracking-widest uppercase">🕒 8AM - 5PM</p>
                </div>
              </div>

              {/* MAP COMPONENT - If the data has coordinates, show it! */}
              {centerData.coords && (
                <div className="rounded-3xl overflow-hidden border border-gray-200 shadow-sm h-64">
                  <OpenMap coordinates={centerData.coords} centerName={centerData.name} />
                </div>
              )}
              
              {/* VIRAL SHARE BUTTON */}
              <button className="w-full py-4 border-2 border-black rounded-2xl font-black uppercase text-sm hover:bg-black hover:text-white transition-all flex items-center justify-center gap-2">
                📢 Share Location to WhatsApp
              </button>
            </div>
          )}
        </div>

        <footer className="mt-16 text-center">
          <p className="text-[10px] text-gray-300 font-bold uppercase tracking-[0.2em]">Privacy First • For Kenya • 2027</p>
        </footer>
      </div>
    </main>
  );
}
