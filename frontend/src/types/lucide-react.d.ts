declare module 'lucide-react' {
    import { ComponentType, SVGProps } from 'react';

    export interface LucideProps extends SVGProps<SVGSVGElement> {
        size?: string | number;
        color?: string;
        strokeWidth?: string | number;
        absoluteStrokeWidth?: boolean;
    }

    export const Power: ComponentType<LucideProps>;
    export const Cpu: ComponentType<LucideProps>;
    export const Shield: ComponentType<LucideProps>;
    export const Globe: ComponentType<LucideProps>;
    // Add other icons as needed or use a catch-all
    export const LucideIcon: ComponentType<LucideProps>;
}
