import React from 'react';
import { graphql } from 'gatsby';

import Layout from '../components/layout';
import PostsList from '../components/postsList';

import Seo from "../components/seo"
import '../styles/styles.scss';

const IndexPage = ({
  data: { allMarkdownRemark: { edges: posts }, seoImage },
}) => (
    <Layout>
    <Seo title="Home" />
    <div class="split">
      <div class="left">
        <h1>Welcome. <span class="emphasis">I'm Justin.</span></h1>
    <p>I'm probably best described over-caffeinated problem solver. I'm an experienced Data Science and Engineering professional who is comfortable working across the stack to build performant, scalable, and reliable solutions that solve real business problems. Check out the blog for some of my musings about Software Engineering and Management, or the Projects page to check out some of my side projects.</p>
    <h2>Latest posts</h2>

      <PostsList posts={posts} />
      </div>
      <div class="right">
        <img class="profile-pic" src="https://avatars.githubusercontent.com/u/22459070?v=4"></img>
      </div>
    </div>
    {/* <section className="content-list">
      <h2>Latest posts</h2>

      <PostsList posts={posts} />
    </section> */}
  </Layout>
);

export default IndexPage;

export const IndexQuery = graphql`
  query IndexPage {
    allMarkdownRemark(
      sort: { order: DESC, fields: [frontmatter___date] }
      limit: 5
    ) {
      edges {
        node {
          id
          fields {
            slug
          }
          frontmatter {
            title
            date(formatString: "MMMM DD, YYYY")
          }
        }
      }
    }
  }
`;