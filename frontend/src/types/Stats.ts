export type Stats = {
    stats: Record<string, Record<string, number>>;
    sdgs_processed: number[];
    total_patents: number;
    countries_found: string[];
};