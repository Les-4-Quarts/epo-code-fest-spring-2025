import type { Patent } from "./Patent";

export type SearchResult = {
    total_count: number;
    first: number;
    last: number;
    total_results: number;
    patents: Patent[];
}