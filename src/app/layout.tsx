import type { Metadata } from 'next';
import './globals.css';
export const metadata:Metadata={title:'Skill City · Your creative playground',icons:{icon:'/images/skill-city-logo.png'},description:'A living city of skills. Explore buildings, meet Claude agents and find your next idea.'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
