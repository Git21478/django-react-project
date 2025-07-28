import styles from "./Pagination.module.css";

function Pagination({ currentPage, setCurrentPage, pages }) {
    return (
        <div className={styles.pagination}>
            {currentPage > 1
                ? <span onClick={() => setCurrentPage(currentPage - 1)}>&lt;</span>
                : <span>&lt;</span>
            }

            {pages.map((page) => (
                page == currentPage
                ? <span className={styles.current_page} key={page}>{page}</span>
                : <span onClick={() => setCurrentPage(page)} key={page}>{page}</span>
            ))}

            {currentPage < pages.length
                ? <span onClick={() => setCurrentPage(currentPage + 1)}>&gt;</span>
                : <span>&gt;</span>
            }
        </div>
    );
};

export default Pagination;