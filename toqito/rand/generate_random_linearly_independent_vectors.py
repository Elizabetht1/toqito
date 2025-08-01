"""Generates a collection of linearly independent vectors."""

import numpy as np


def generate_random_linearly_independent_vectors(
    num_vectors: np.ndarray, dim: int, is_real: bool = True, seed: int | None = None, max_attempts: int | None = None
) -> list[np.ndarray]:
    r"""Generate a set of linearly independent random vectors.

    This function generates a random collection of linearly independent (possibly complex) vectors.

    Examples
    ==========
    Using :code:`|toqito⟩`, we may generate a random, linearly independent set of (compelx or real-valued)
    :math:`n`- dimensional vectors. To generate a set of 3 vectors
    with :math:`d=4`, this can be accomplished as follows.

    .. jupyter-execute::

     from toqito.rand import generate_random_linearly_independent_vectors

     li_vecs = generate_random_linearly_independent_vectors(3,4)

     li_vecs

    To verify the vectors are in fact linearly indepependent, we use the :code:`is_linearly_independent` function from
    :code:`|toqito⟩` as follows

    .. jupyter-execute::

     from toqito.matrix_props import is_linearly_independent
     import numpy as np

     is_linearly_independent(np.expand_dims(li_vecs.T,axis=2).tolist())

    It is also possible to generate a set of complex vectors, as follows.

    .. jupyter-execute::

     from toqito.rand import generate_random_linearly_independent_vectors

     li_vecs = generate_random_linearly_independent_vectors(3,4,is_real=False)

     li_vecs

    The procedure to verify the vectors are linearly independent is identical to the real-valued case.

    :param num_vectors: The number of vectors to generate.
    :param dim: The dimension of the vector space.
    :param is_real: Boolean denoting whether the returned vector will have all real entries or not.
                    Default is :code:`False`.
    :param seed: int | None
        A seed used to instantiate numpy's random number generator.
    :param max_attempts: int | None
        The maximum number of times to attempt generation. If not set, will
        default to num_vectors * dim
    :return: A (dim x num_vectors) matrix whose columns are the generated independent vectors.

    """
    if num_vectors > dim:
        raise ValueError("Cannot have more independent vectors than the dimension of the space.")

    # Keep generating until we get a matrix with independent columns.

    random_num_generator = np.random.default_rng(seed=seed)  ## construct a random number generator

    if not max_attempts:
        max_attempts = num_vectors * dim

    for _ in range(max_attempts):
        if is_real:
            rand_mat = random_num_generator.standard_normal(size=(dim, num_vectors))
        else:
            rand_mat = random_num_generator.standard_normal(
                size=(dim, num_vectors)
            ) + 1j * random_num_generator.standard_normal(size=(dim, num_vectors))

        # Check that the rank equals num_vectors.
        if np.linalg.matrix_rank(rand_mat) == num_vectors:
            return rand_mat

    raise ValueError(
        f"Failed to generate {num_vectors} linearly independent vectors "
        f"of dimension {dim} after {max_attempts} attempts."
    )
