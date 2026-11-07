"use client";

import { useEffect, useState } from "react";
import { apiClient } from "@/lib/api";

type Product = {
  id: number;
  name: string;
  description: string;
  category: string;
  price: number;
  stock_quantity: number;
  is_organic: boolean;
};

export default function ProductsPage() {
  const [items, setItems] = useState<Product[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    apiClient
      .get<Product[]>("/products", {
        params: search.trim() ? { search: search.trim() } : {},
      })
      .then(({ data }) => {
        if (active) setItems(data);
      })
      .catch(() => {
        if (active)
          setError(
            "Could not load the catalog. Check that the API is running.",
          );
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [search]);

  return (
    <section className="mx-auto w-full max-w-6xl flex-1 px-4 py-10">
      <h1 className="text-3xl font-bold">Spice Catalog</h1>
      <p className="mt-2 text-slate-600">
        Browse our available spices and blends.
      </p>
      <input
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        aria-label="Search products"
        placeholder="Search by name, description, or category"
        className="mt-6 w-full max-w-xl rounded-md border bg-white px-4 py-3"
      />
      {loading && <p className="mt-8 text-slate-500">Loading catalog…</p>}
      {error && (
        <p role="alert" className="mt-8 rounded bg-red-50 p-3 text-red-700">
          {error}
        </p>
      )}
      {!loading && !error && items.length === 0 && (
        <p className="mt-8 rounded-lg border bg-white p-6 text-slate-600">
          No products found. Add products to the catalog database to display
          them here.
        </p>
      )}
      <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {items.map((product) => (
          <article
            key={product.id}
            className="rounded-xl border bg-white p-5 shadow-sm"
          >
            <p className="text-xs font-semibold uppercase tracking-wide text-orange-700">
              {product.category}
              {product.is_organic ? " · Organic" : ""}
            </p>
            <h2 className="mt-2 text-xl font-bold">{product.name}</h2>
            <p className="mt-3 text-sm leading-6 text-slate-600">
              {product.description}
            </p>
            <div className="mt-5 flex justify-between border-t pt-4 text-sm">
              <strong>${product.price.toFixed(2)}</strong>
              <span
                className={
                  product.stock_quantity > 0
                    ? "text-emerald-700"
                    : "text-slate-500"
                }
              >
                {product.stock_quantity > 0
                  ? `${product.stock_quantity} in stock`
                  : "Out of stock"}
              </span>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
