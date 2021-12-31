import React from 'react';
import { Link } from 'gatsby';

const PostsList = ({ posts }) => (
  <ul className="post-list">
    {posts.map(post => (
      <li key={post.node.id}>
        <Link to={post.node.fields.slug}>
          {post.node.frontmatter.title}
          ({post.node.frontmatter.date})
        </Link>
      </li>
    ))}
  </ul>
);

export default PostsList;