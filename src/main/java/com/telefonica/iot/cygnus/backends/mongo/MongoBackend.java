/**
 * Copyright 2015 Telefonica Investigación y Desarrollo, S.A.U
 *
 * This file is part of fiware-cygnus (FI-WARE project).
 *
 * fiware-cygnus is free software: you can redistribute it and/or modify it under the terms of the GNU Affero
 * General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
 * option) any later version.
 * fiware-cygnus is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
 * implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License
 * for more details.
 *
 * You should have received a copy of the GNU Affero General Public License along with fiware-cygnus. If not, see
 * http://www.gnu.org/licenses/.
 *
 * For those usages not covered by the GNU Affero General Public License please contact with iot_support at tid dot es
 */
package com.telefonica.iot.cygnus.backends.mongo;

import java.util.ArrayList;
import org.bson.Document;

/**
 * Interface for those backends implementing the persistence in MongoDB.
 * 
 * @author frb
 */

public interface MongoBackend {
    
    /**
     * Creates a database, given its name, if not exists.
     * @param dbName
     * @throws Exception
     */
    void createDatabase(String dbName) throws Exception;
    
    /**
     * Creates a collection, given its name, if not exists in the given database.
     * @param dbName
     * @param collectionName
     * @throws Exception
     */
    void createCollection(String dbName, String collectionName) throws Exception;
    
    /**
     * Inserts a new document in the given raw collection within the given database (row-like mode).
     * @param dbName
     * @param collectionName
     * @param aggregation
     * @throws Exception
     */
    void insertContextDataRaw(String dbName, String collectionName, ArrayList<Document> aggregation) throws Exception;
    
    /**
     * Inserts a new document in the given aggregated collection within the given database (row-like mode).
     * @param dbName
     * @param collectionName
     * @param recvTimeTs
     * @param recvTime
     * @param entityId
     * @param entityType
     * @param attrName
     * @param attrType
     * @param attrValue
     * @param attrMd
     * @throws Exception
     */
    void insertContextDataAggregated(String dbName, String collectionName, long recvTimeTs, String recvTime,
            String entityId, String entityType, String attrName, String attrType, String attrValue, String attrMd)
        throws Exception;
    
    /**
     * Stores in per-service/database "collection_names" collection the matching between a hash and the fields used to
     * build it.
     * FIXME: destination is under study
     * @param dbName
     * @param hash
     * @param isAggregated
     * @param fiwareService
     * @param fiwareServicePath
     * @param entityId
     * @param entityType
     * @param attrName
     * @param destination
     * @throws java.lang.Exception
     */
    void storeCollectionHash(String dbName, String hash, boolean isAggregated, String fiwareService,
            String fiwareServicePath, String entityId, String entityType, String attrName, String destination)
        throws Exception;
} // MongoBackend