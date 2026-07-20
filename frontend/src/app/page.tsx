import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center flex-1 px-4 text-center">
      <h1 className="text-5xl font-extrabold tracking-tight sm:text-6xl text-slate-900 mb-6">
        Discover the World of{" "}
        <span className="text-orange-600">Premium Spices</span>
      </h1>
      <p className="mt-4 text-lg text-slate-600 max-w-2xl mb-10">
        From Ceylon Cinnamon to Madagascar Vanilla. Not sure what you need? Our
        AI assistant is here to recommend products, share recipes, and answer
        your cooking questions.
      </p>

      <div className="flex gap-4">
        <Link
          href="/chat"
          className="rounded-md bg-orange-600 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-orange-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange-600 transition-all"
        >
          Talk to AI Assistant
        </Link>
        <Link
          href="/products"
          className="rounded-md bg-white px-6 py-3 text-sm font-semibold text-slate-900 shadow-sm ring-1 ring-inset ring-slate-300 hover:bg-slate-50 transition-all"
        >
          Browse Catalog
        </Link>
      </div>
    </div>
  );
}
